# coding: utf-8

import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
FRONT_DIR = "{}/front/dist".format(ROOT_DIR)

DEBUG = False
LOGIN_URL = "http://data.gtapp.xyz/login"

HOST = "0.0.0.0"
PORT = 5000

# 日志配置
LOG_PATH = os.path.join(ROOT_DIR, 'logs')
if not os.path.isdir(LOG_PATH):
    os.mkdir(LOG_PATH)

DEBUG_LOG = os.path.join(LOG_PATH, "debug.log")
INFO_LOG = os.path.join(LOG_PATH, "info.log")
WARNING_LOG = os.path.join(LOG_PATH, "warning.log")
ERROR_LOG = os.path.join(LOG_PATH, "error.log")