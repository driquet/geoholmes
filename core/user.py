#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
File: cache.py
Author: Damien Riquet <d.riquet@gmail.com>
Description: User class
'''

class User:
    """
    A user represents a geocaching player
    We need to store data about him:
        - last solved challenge
        - beginning of the current challenge (timestamp)
        - input of the current challenge
    """

    def __init__(self):
        self.name = ''
        self.last_solved = -1
        self.current_timestamp = 0
        self.current_input = ''


    def get_json_data(self):
        return self.__dict__


def new_user(name):
    user = User()
    user.name = name
    return user

def load_user_from_json(data):
    user = User()
    for key, value in data.items():
        setattr(user, key, value)
    return user
