# coding: utf-8

DEBUG = True

MONGO_CONFIG = {
    'account': {
        "host_port": [('39.96.63.13', 37017)],
        "database": "account",
        "user_name": "admin",
        "password": "123qwe"
    },
    'admin': {
        "host_port": [('39.96.63.13', 37017)],
        "database": "account",
        "user_name": "admin",
        "password": "123qwe"
    }
}

REDIS_CONFIG = {
    'auth': {
        "host": "39.96.63.13",
        "port": 6379,
        "password": 'root',
        "database": 0
    }
}