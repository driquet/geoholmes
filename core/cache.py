#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
File: cache.py
Author: Damien Riquet <d.riquet@gmail.com>
Description: cache class
'''

import os, json, time
from geoholmes.core import user, challenge, utils

class Cache:
    def __init__(self, cache_dir):
        """
        Create an instance of cache class using data from a directory
        This directory must have this structure:
            cache_dir/
            - readme.rst (Description of the cache, the challenge and so on)
            - cache.json (Data about the cache: title, code)
            - src/ (Source for challenge(s))
            - users.json (Data about users)
        """
        self.cache_dir = cache_dir
        self.challenge_dir = 'src'
        self.media_dir = 'media'

        # Reading data from other files
        self.init_cache_data()
        self.init_challenges()
        self.init_users()

        # If content fields are empty, we try to find corresponding rst files
        for field in ['description', 'output']:
            if not getattr(self, field):
                # Empty field
                filename = "%s.rst" % (field)
                setattr(self, field, utils.read_rst(os.path.join(cache_dir, filename)))


    def init_cache_data(self, cache_file='cache.json'):
        """ Read cache data using a json file """
        with open(os.path.join(self.cache_dir, cache_file)) as f:
            json_content = ''.join(f.readlines())
            cache_data = json.loads(json_content)

            for field in ['name', 'description', 'code', 'author', 'mail', 'hint', 'challenges', 'output']:
                setattr(self, field, cache_data[field])

            self.url = 'http://coord.info/%s' % self.code
            self.mail = self.mail.replace('@', '_at_').replace('.', '_dot_')


    def init_challenges(self, challenge_dir='src'):
        """ Load challenges """
        challenges = []
        for challenge_type, challenge_arg in self.challenges:
            challenges.append(challenge.__getattribute__(challenge_type)(os.path.join(self.cache_dir, challenge_dir), challenge_arg))
        self.challenges = challenges


    def init_users(self, users_file='users.json'):
        """ Load users file """
        # First test if the file exists, if it does not, create an empty
        # structure
        file_path = os.path.join(self.cache_dir, users_file)
        if not os.path.isfile(file_path):
            self.users = {}
        else:
            with open(file_path) as f:
                users_data = json.load(f)
                self.users = {}

                for user_json in users_data:
                    u = user.load_user_from_json(user_json)
                    self.users[u.name] = u


    def save_users(self, users_file='users.json'):
        """ Save users into a json file """
        all_user = [u.get_json_data() for u in self.users.values()]
        file_path = os.path.join(self.cache_dir, users_file)

        with open(file_path, 'w') as f:
            f.write(json.dumps(all_user))


    def get_user(self, user_name):
        """ Return a user (create it if necessary) """
        if user_name not in self.users:
            self.users[user_name] = user.new_user(user_name)

        return self.users[user_name]


    def get_user_challenge_nb(self, user):
        u = self.get_user(user['username'])
        return u.last_solved + 1


    def get_challenge(self, user):
        """ Get the next challenge for a user """
        u = self.get_user(user['username'])

        # Computing the next challenge
        challenge_nb = u.last_solved + 1
        if challenge_nb >= len(self.challenges):
            # There is no challenge left
            return None

        # Retrieving the current challenge
        current_challenge = self.challenges[challenge_nb]

        if current_challenge.get_challenge_duration() != - 1 and \
           time.time() - u.current_timestamp > current_challenge.get_challenge_duration():
            u.current_input = None
            u.current_timestamp = time.time()

        problem, hint, challenge_input = current_challenge.get_challenge(u.name, u.current_input)
        u.current_input = challenge_input
        self.save_users()

        summary = current_challenge.get_challenge_summary()
        summary['hint'] = hint
        summary['problem'] = problem

        # Compute the time left
        if summary['duration'] != -1:
            summary['time_left'] = u.current_timestamp + summary['duration'] - time.time()

        return summary


    def get_statistics(self):
        """ Return some stats about the cache """
        users = [u.last_solved for u in self.users.values()]
        stats = {}
        for i in xrange(len(self.challenges)):
            stats[i]= len([u for u in users if u >= i])

        return stats



    def check_challenge(self, user, answer):
        """ Check the answer of a user """
        u = self.get_user(user['username'])

        # Computing the next challenge
        challenge_nb = u.last_solved + 1
        if challenge_nb >= len(self.challenges):
            # There is no challenge left
            return False

        # Retrieving the current challenge
        current_challenge = self.challenges[challenge_nb]

        if current_challenge.get_challenge_duration() != - 1 and \
           time.time() - u.current_timestamp > current_challenge.get_challenge_duration():
            return False

        if current_challenge.check_challenge(user, u.current_input, answer):
            u.last_solved += 1
            self.save_users()
            return True

        return False


    def get_solved_challenges(self, user):
        """ Return the solved challenges """
        u = self.get_user(user['username'])
        return self.challenges[:u.last_solved+1]

    def get_unsolved_challenges(self, user):
        """ Return the solved challenges """
        u = self.get_user(user['username'])
        return self.challenges[u.last_solved+1:]


    def get_media_path(self):
        return os.path.join(self.cache_dir, self.media_dir)
