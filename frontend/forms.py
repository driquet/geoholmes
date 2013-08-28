#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
File: forms.py
Author: Damien Riquet <d.riquet@gmail.com>
Description: Web forms
'''

from flask.ext.wtf import Form, TextField, Required

class LoginForm(Form):
    username = TextField('Username', validators=[Required(message='Username is required.')])

class ChallengeForm(Form):
    answer = TextField('Answer', validators=[Required(message='An answer is required.')])
