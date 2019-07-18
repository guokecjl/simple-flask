# coding: utf-8

from apps.base_handler import BaseHandler

class HelloWorldHandler(BaseHandler):

    def get(self):
        return self.write_response(data={
            'hello': '你好'
        })
