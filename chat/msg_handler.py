#!/usr/bin/env python

"""
author: ares
date: 2019/9/21
desc:
"""


class MsgHandler(object):
    """Msg Handler"""
    def __init__(self, name):
        self.name = name
        self._running = False
        self._stopped = False
        self._observers = []

    def register(self, observer):
        """register observer"""
        self._observers.append(observer)

    def start(self, redis_cli):
        """msg handler loop"""
        self._running = True

        while True:
            for observer in self._observers:
                try:
                    ob_name = observer.name
                    msg_key_list = redis_cli.keys('msg:*{reciver}'.format(reciver=ob_name))
                    for msg_key in msg_key_list:
                        _, sender, reciver = msg_key.split(':')
                        msg_dict = redis_cli.hmget(msg_key)
                        m_type, data = msg_dict['type'], msg_dict['data']
                        observer.update(data, reciver, m_type)
                except KeyError as e:
                    print('KeyError: {}'.format(e))
                except Exception as e:
                    print('UnknowError: {}'.format(e))

            # 检测状态
            if self._stopped:
                self._running = False
                break

    def close(self):
        """close handler"""
        if self._running:
            self._stopped = True
