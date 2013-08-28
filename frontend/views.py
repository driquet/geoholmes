#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
File: view.py
Author: Damien Riquet <d.riquet@gmail.com>
Description: Views for the web frontend
'''

import os, re
from functools import wraps
from flask import Blueprint, current_app, render_template, send_from_directory, abort, session, request, url_for, redirect, flash
from geoholmes.core import cache
from geoholmes.frontend import forms, user
from geoholmes.app import gc_api, app

# This blueprint contains all route of the app
frontend = Blueprint('frontend', __name__, template_folder='templates')

# ----------------------
#  Useful methods
# ----------------------
def render_theme(template, **kwargs):
    template_path = os.path.join(current_app.config['FRONTEND_THEME'], template)
    return render_template(template_path, **kwargs)

def get_caches():
    caches = []
    for d in os.listdir(current_app.config['CACHE_PATH']):
        cache_dir = os.path.join(current_app.config['CACHE_PATH'], d)
        caches.append(cache.Cache(cache_dir))
    return caches

def get_cache(cache_code):
    caches = get_caches()
    for cache in caches:
        if cache.code == cache_code:
            return cache
    return None

def cache_substitute(cache):
    for key in ['description', 'output']:
        setattr(cache, key, data_substitute(cache, getattr(cache, key)))


def challenge_substitute(cache, challenge):
    for key in ['description', 'output']:
        challenge[key] = data_substitute(cache, challenge[key])


def data_substitute(cache, content):
    # Cache media
    for m in re.finditer(r"{{cache_media:([^}]*)}}", content):
        url_media = url_for('.get_cache_media', cache=cache.code, media=m.group(1))
        content = content.replace(m.group(0), url_media)

    # Flags
    for m in re.finditer(r"{{flag:([^}]*)}}", content):
        content = content.replace(m.group(0), get_flag(m.group(1).upper()))

    return content


def get_flag(iso):
    flag_path = 'img/flags/%s.png' % iso
    return '<img src="%s" class="img-rounded" />' % url_for('.static_files', filename=flag_path)

@app.context_processor
def utility_processor():
    return dict(get_flag=get_flag)

# ----------------------
#  Filters
# ----------------------
def customize_content(s):
    substitutions = {
        '{{ geocacher_username }}' : '<strong>%s</strong>' % session['user']['username'],
    }
    for key, value in substitutions.items():
        s = s.replace(key, value)
    return s
app.jinja_env.filters['customize'] = customize_content




# ----------------------
#  Routes
# ----------------------

@frontend.route('/static_files/<path:filename>')
def static_files(filename):
    """ Deals with static files (like css and js) """
    static_path = os.path.join(frontend.root_path, 'templates', current_app.config['FRONTEND_THEME'], 'static')
    return send_from_directory(static_path, filename)


# ----- Login related routes
@frontend.route('/login/')
def login():
    if session.has_key('user'):
        session.pop('user', None)
    callback_url = url_for('.oauthorized', next=request.args.get('next'), _external=True)
    return gc_api.authorize(callback=callback_url)

@frontend.route('/oauthorized')
@gc_api.authorized_handler
def oauthorized(resp):
    next_url = request.args.get('next') or url_for('.home')
    if resp is None:
        flash('You denied the request to sign in', 'error')
    else:
        session['user'] = user.create_user(resp['oauth_token'], resp['oauth_token_secret'])
        user.init_user(gc_api, session['user'])
    return redirect(next_url)

@gc_api.tokengetter
def get_api_token():
    if session.has_key('user'):
        return session['user']['token'], session['user']['secret']
    return None


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if not session.has_key('user'):
            return redirect(url_for('.login', next=request.url))

        return f(*args, **kwargs)
    return decorated_function


@frontend.route('/logout')
def logout():
    if session.has_key('user'):
        session.pop('user', None)
    return redirect(url_for('.home'))

# ---- CACHES ROUTES ----
@frontend.route('/')
def home():
    caches = get_caches()
    return render_theme('home.html', caches=caches)

@frontend.route('/cache/<cache>', methods=['GET', 'POST'])
@login_required
def show_cache(cache):
    cache = get_cache(cache)

    if not cache:
        abort(404)

    form = forms.ChallengeForm(request.form)
    just_solved = False

    cache_substitute(cache)

    if request.method == 'POST' and form.validate():
        if cache.check_challenge(session['user'], form.answer.data):
            just_solved = True
            flash('Congratulation, you just solved a challenge !', 'success')
        else:
            flash('Too bad, your answer is not correct... Try again !', 'error')

    ctx = {
        'all_challenges' : [c.get_challenge_summary() for c in cache.challenges],
        'current_challenge' : cache.get_challenge(session['user']),
        'current_number': cache.get_user_challenge_nb(session['user']),
        'form' : forms.ChallengeForm(),
        'cache' : cache,
        'stats' : cache.get_statistics(),
        'just_solved' : just_solved,
    }

    for challenge in ctx['all_challenges']:
        challenge_substitute(cache, challenge)
    if ctx['current_challenge'] is not None:
        challenge_substitute(cache, ctx['current_challenge'])

    return render_theme('cache.html', **ctx)

@frontend.route('/cache_files/<cache>/<media>')
@login_required
def get_cache_media(cache, media):
    cache = get_cache(cache)
    path = cache.get_media_path()
    return send_from_directory(path, media)
