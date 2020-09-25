#!/usr/bin/env python

"""
author: ares
date: 2019/8/28
desc:
"""

import time
from celery import Celery

from config import BROKER_URL, CELERY_RESULT_BACKEND

app = Celery('tasks', backend=CELERY_RESULT_BACKEND, broker=BROKER_URL)


@app.task
def send_msg(msg, user):
    print('send msg to %s ...' % user)
    time.sleep(3)
    print('send finished')
