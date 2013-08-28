#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
File: user.py
Author: Damien Riquet <d.riquet@gmail.com>
Description: Current user logged in
'''

from geoholmes.frontend import api


def create_user(token, secret):
    return {
        'username' : '',
        'token'    : token,
        'secret'   : secret
    }


def init_user(gc_api, user):
    # Retrieve username
    options = {
        "ProfileOptions":{},
        "DeviceInfo":{
            "ApplicationCurrentMemoryUsage" : 2*2048,
            "ApplicationPeakMemoryUsage"    : 2*2048,
            "ApplicationSoftwareVersion"    : "1.0",
            "DeviceManufacturer"            : "PC",
            "DeviceName"                    : "PC",
            "DeviceOperatingSystem"         : "Unknown",
            "DeviceTotalMemoryInMB"         : 2*2048,
            "DeviceUniqueId"                : "blabla",
            "MobileHardwareVersion"         : "blabla",
            "WebBrowserVersion"             : "blabla"
        },
    }
    data = api.post_request(gc_api, user['token'], 'GetYourUserProfile', options)
    if not data:
        return None

    user['username'] = data['Profile']['User']['UserName']
