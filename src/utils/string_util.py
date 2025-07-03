import base64
import hashlib
import random
import re
import string
import uuid


def cook_element(element: tuple, *value):
    locator, element = element
    return locator, str(element).format(*value)


def decode(encrypted_value):
    return base64.b64decode(encrypted_value).decode('utf-8')


def random_string(size=8, *, only_letter=False):
    # Random a string with size default is 8 - ex: abcdefgx
    if only_letter:
        return "".join([random.choice(string.ascii_letters + string.ascii_letters[::-1]) for _ in range(size)])
    return "".join([random.choice(string.ascii_letters + string.digits) for _ in range(size)])


def unique_uid():
    return str(uuid.uuid1()).split("-")[0]


def hash_md5(value):
    return hashlib.md5(value.encode()).hexdigest()


def encrypt_rsa_base64(raw_value, keypath):
    if isinstance(keypath, bytes) or isinstance(keypath, str):
        publickey = keypath
    else:
        with open(keypath, "rb") as f:
            publickey = f.read()

    from Crypto.Cipher import PKCS1_v1_5
    from Crypto.PublicKey import RSA
    pubKeyObj = RSA.importKey(publickey)
    cipher = PKCS1_v1_5.new(pubKeyObj)

    if isinstance(raw_value, bytes):
        value = raw_value
    else:
        value = raw_value.encode("utf-8")
    e_value = cipher.encrypt(value)
    return base64.b64encode(e_value).decode("utf-8")


def format_number_string(text):
    return re.sub(r"[^\d.]", "", text)
