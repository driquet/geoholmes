def get_challenge(user_name, challenge_input=None):
    return 'question','hint', 'input'

def get_challenge_title():
    return 'test'

def get_challenge_duration():
    return 60

def get_challenge_description():
    return 'Top descriptino'

def check_challenge(user_name, challenge_input, challenge_response):
    print challenge_response
    if challenge_response == 'pwet': return True
    return False

def get_challenge_output():
    return 'outpu'
