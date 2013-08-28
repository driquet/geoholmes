#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
File: utils.py
Author: Damien Riquet <d.riquet@gmail.com>
Description: A lot of tools in order to make cache owner life easier
'''

from docutils.core import publish_parts

def read_rst(file_path, initial_header_level=1):
    """ Read a restructuredtext file and return converted html data """
    try:
        with open(file_path) as f:
            content = ''.join(f.readlines())
            overrides = {'initial_header_level' : initial_header_level}
            parts = publish_parts(content , writer_name='html', settings_overrides=overrides)
            return parts['html_body']
    except:
        return ''



