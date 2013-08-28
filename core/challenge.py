#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
File: challenge.py
Author: Damien Riquet <d.riquet@gmail.com>
Description: Challenge class
'''

import imp, os, json, random
from geoholmes.core import utils

class Challenge(object):
    """ 'Abstract' class """

    def __init__(self, path, name):
        # if some fields are empty, we try to read corresponding rst
        # files (if they exist)
        for key in ['description', 'output']:
            if key in self.challenge and not self.challenge[key]:
                # Empty field
                filename = "%s_%s.rst" % (os.path.splitext(name)[0], key)
                self.challenge[key] = utils.read_rst(os.path.join(path, filename))


    def get_challenge(self, user, challenge_input=None):
        """
        Return the challenge according to a user_name
        Arguments:
            - user: could be used to customize the challenge
            - challenge_input: input used to determine the challenge
        Return:
            a tuple: (problem, hint, challenge_input)
        """
        pass


    def get_challenge_title(self):
        pass


    def get_challenge_duration(self):
        pass


    def get_challenge_description(self):
        """ Return the description of this challenge """
        pass

    def check_challenge(self, user, challenge_input, challenge_response):
        """
        Check if the challenge is achieved by the user
        Arguments:
            - user
            - challenge_input: input used to determine the challenge
            - challenge_response: provided by the user
        Return:
            a boolean: is the challenge achieved
        """
        pass

    def get_challenge_output(self):
        """ Return the final output of the challenge (when it is achieved) """
        pass


    def get_challenge_summary(self):
        return {
            'title': self.get_challenge_title(),
            'duration': self.get_challenge_duration(),
            'description': self.get_challenge_description(),
            'output': self.get_challenge_output(),
        }



class CustomScriptPython(Challenge):
    """
    This class use a custom script provided by the owner to create a challenge
    This script must provide some functions. See the template.
    """

    def __init__(self, path, script_path):
        # Load the script
        loaded_script = imp.load_source('%s_%s' %  (path,script_path), os.path.join(path, script_path))
        setattr(self, 'challenge_module', loaded_script)

        self.challenge = {}
        for key in ['title', 'description', 'output', 'duration']:
            fct_name = 'get_challenge_%s' % key
            self.challenge[key] = self.challenge_module.__dict__[fct_name]()

        super(CustomScriptPython, self).__init__(path, script_path)


    def get_challenge(self, user, challenge_input=None):
        return self.challenge_module.get_challenge(user, challenge_input)

    def get_challenge_title(self):
        return self.challenge['title']

    def get_challenge_duration(self):
        return self.challenge['duration']

    def get_challenge_description(self):
        return self.challenge['description']

    def check_challenge(self, user, challenge_input, challenge_response):
        return self.challenge_module.check_challenge(user, challenge_input, challenge_response)

    def get_challenge_output(self):
        return self.challenge['output']


class ProblemChallenge(Challenge):
    """
    This class use a json file (provided by the owner) to ask a question
    It could have one or several question.
    Json file must be formatted as follow:
        fields: title, description, duration, output, questions
        questions is a list of tuple (question, answer, hint)
    """
    def __init__(self, path, data_file):
        # Load the script
        with open(os.path.join(path, data_file)) as f:
            self.challenge = json.load(f)

        super(ProblemChallenge, self).__init__(path, data_file)

    def get_challenge(self, user, challenge_input=None):
        if not isinstance(challenge_input, int):
            # At this point, no input was provided
            # It means that we need to choose a problem randomly
            challenge_input = random.randint(0, len(self.challenge['problems']) - 1)

        question, answer, hint = self.challenge['problems'][challenge_input]
        return question, hint, challenge_input

    def get_challenge_title(self):
        return self.challenge['title']

    def get_challenge_duration(self):
        return self.challenge['duration']

    def get_challenge_description(self):
        return self.challenge['description']

    def get_challenge_output(self):
        return self.challenge['output']

    def check_challenge(self, user, challenge_input, challenge_response):
        question, answer, hint = self.challenge['problems'][challenge_input]
        return answer.lower() == challenge_response.lower()


if __name__ == '__main__':
    script = '/Users/driquet/git/geocaching_mystery/geoholmes/caches/example/src/challenge_1.py'
    c = CustomScriptPython(script)

    c.get_challenge('')
    c.get_challenge_title()
    c.get_challenge_description()
    c.get_challenge_output()
    c.check_challenge('','','')
