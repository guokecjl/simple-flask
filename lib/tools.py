# coding: utf-8

import hashlib
import datetime


def encrypt_password(pwd):
    return hashlib.md5(pwd.encode()).hexdigest()


def generate_now():
    t = datetime.datetime.now()
    return t.strftime('%Y-%m-%d %H:%M:%S')
