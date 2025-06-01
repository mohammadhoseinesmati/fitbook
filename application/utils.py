from werkzeug.security import generate_password_hash,check_password_hash
import json
import random
import string


def Password_Hash(password):
        return generate_password_hash(password)


def check_Password(pashash,password):
        return check_password_hash(pashash , password)

def decoder(payload):
    return json.loads(payload.decode('utf-8'))




def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits 
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


