#!/usr/bin/env python

"""
author: ares
date: 2019/9/21
desc:
"""

import time

from database_clients.redis_cli import redis_cli


class MsgHandler(object):
    """Msg Handler"""
    def __init__(self, name):
        self.name = name
        self._running = False
        self._stopped = False
        self.observers = []

    def start(self, pipe):
        """msg process loop"""
        self._running = True
        while True:
            try:
                print(self.observers)
                is_recive = pipe.poll(timeout=1)
                print(is_recive)
                if is_recive:
                    instance = pipe.recv()
                    self.observers.append(instance)
                for observer in self.observers:
                    ob_name = observer.name
                    msg_key_list = redis_cli.keys('msg:*:{reciver}'.format(reciver=ob_name))
                    for msg_key in msg_key_list:
                        print(msg_key)
                        _, sender, reciver = bytes.decode(msg_key).split(':')
                        msg_dict = redis_cli.hgetall(msg_key)
                        m_type, msg = msg_dict[b'msg_type'], msg_dict[b'msg']
                        observer.receive(msg, sender, m_type)
            except KeyError as e:
                print('KeyError: {}'.format(e))
            except Exception as e:
                print('UnknowError: {}'.format(e))

            # 检测状态
            if self._stopped:
                self._running = False
                break

            time.sleep(1)

    def close(self):
        """close handler"""
        if self._running:
            self._stopped = True

