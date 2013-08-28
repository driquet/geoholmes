#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
File: api.py
Author: Damien Riquet <d.riquet@gmail.com>
Description: API interaction
'''

def post_request(api, token, method, options):
    options['AccessToken'] = token
    method_url = '%s?format=Json' % method
    resp = api.post(method_url, data=options, format='json')

    if resp.status != 200:
        return None
    return resp.data

