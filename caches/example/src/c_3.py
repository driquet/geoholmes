import random

def caesar(plaintext,shift):

    alphabet=["a","b","c","d","e","f","g","h","i","j","k","l",
        "m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

    #Create our substitution dictionary
    dic={}
    for i in range(0,len(alphabet)):
        dic[alphabet[i]]=alphabet[(i+shift)%len(alphabet)]

    #Convert each letter of plaintext to the corrsponding
    #encrypted letter in our dictionary creating the cryptext
    ciphertext=""
    for l in plaintext.lower():
        if l in dic:
            l=dic[l]
        ciphertext+=l

    return ciphertext

def get_challenge(user_name, challenge_input=None):
    if not challenge_input:
        challenge_input= random.randint(1,25)

    message = "THE ANSWER IS YOU : %s" % (user_name)
    return caesar(message, challenge_input),'', challenge_input

def get_challenge_title():
    return 'Customized challenge'

def get_challenge_duration():
    return 60

def get_challenge_description():
    return 'You received another message. Decode it but you have to be quick, this challenged is timed.'

def check_challenge(user, challenge_input, challenge_response):
    return user['username'] == challenge_response

def get_challenge_output():
    return 'C=3'
