#!/usr/bin/env python

"""
author: ares
date: 2019/10/13
desc:
"""

import time
from typing import Union

import json
from multiprocessing import Process, Pipe

import tornado.web
import tornado.ioloop
import tornado.websocket

from lib.logger import logger
from database_clients.redis_cli import redis_cli

from chat.observer import Broker
from chat.msg_handler import MsgHandler

# parent_conn, child_conn = Pipe()
#
#
# handler = MsgHandler('Chatter')
# p = Process(target=handler.start, args=(child_conn,))
# p.start()


broker = Broker('chatter_manager')


class ConnectionHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args: str, **kwargs: str):
        logger.info('connection opened from {}'.format(self.request.host_name))

    def on_message(self, message: Union[str, bytes]):
        data = json.loads(bytes.decode(message, encoding='utf-8'))
        sender_id, reciver_id, send_time, msg_type, msg = data['sender_id'], \
                                                          data['reciver_id'], \
                                                          data['send_time'], \
                                                          data['msg_type'], \
                                                          data['msg']

        broker.create(sender_id, self)
        reciver = broker.get(reciver_id)

        if reciver:
            reciver.receive(msg, sender_id, msg_type)
        else:

            redis_cli.rpush('msg:{sender}:{reciver}'.format(sender=sender_id, reciver=reciver_id),
                            "{msg_type}:{msg}".format(msg_type=msg_type, msg=msg))

            self.write_message("user {reciver} is not online, but your message has been sent!!!".format(
                reciver=reciver_id))

    def on_close(self):
        print("WebSocket closed")


urls = [
    (r'/api/chat', ConnectionHandler)
]

app = tornado.web.Application(urls).listen(8888)
tornado.ioloop.IOLoop.current().start()
