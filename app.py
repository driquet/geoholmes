# 2013.08.08 12:13:25 CEST
"""
Geoholmes: Geocaching mysteries
Licence: BSD (see LICENCE file)

Author: Damien Riquet <d.riquet@gmail.com>
Description:
    Create the Flask application
"""
import os
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_oauthlib.client import OAuth

# App creation
app = Flask(__name__)
app.debug = True
app.config.from_pyfile(os.path.join(os.getcwd(), 'config.py'))

# OAuth
oauth = OAuth()
gc_api = oauth.remote_app(
    'geocaching',
    consumer_key=app.config['API_CONSUMER_KEY'],
    consumer_secret=app.config['API_CONSUMER_SECRET'],
    base_url=app.config['API_BASE_URL'],
    request_token_url=app.config['API_REQUEST_TOKEN_URL'],
    access_token_url=app.config['API_ACCESS_TOKEN_URL'],
    authorize_url=app.config['API_AUTHORIZE_URL'])

# Toolbar
toolbar = DebugToolbarExtension(app)

# Registering route (via blueprint)
import geoholmes.frontend.views as views
app.register_blueprint(views.frontend, url_prefix=app.config['FRONTEND_PREFIX'])
