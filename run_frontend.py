#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Geoholmes: Geocaching mysteries
Licence: BSD (see LICENCE file)

Author: Damien Riquet <d.riquet@gmail.com>
Description:
    Run the web frontend
'''

from geoholmes.app import app

def main():
    app.run(host=app.config['FRONTEND_HOST'], port=app.config['FRONTEND_PORT'])

if __name__ == '__main__':
    main()
