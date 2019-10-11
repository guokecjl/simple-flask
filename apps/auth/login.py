# coding: utf-8

from webargs.flaskparser import use_args
from marshmallow import fields

from apps.base_handler import BaseHandler
from lib.logger import logger


class LoginHandler(BaseHandler):

    args_format = {
        'user_name': fields.Str(required=False, validate=bool),
        'password': fields.Str(required=False, validate=bool)

    }


    @use_args(args_format)
    def get(self, args):
        try:
            return self.write_response(status=0, err_code=666, err_msg='登陆调试成功', data='ppp')
        except Exception:
            logger.exception('登陆出错')

    @use_args(args_format)
    def post(self, args):
        try:
            user_name, pwd = args['user_name'], args['password']
            print(user_name, pwd)
            return self.write_response({})
        except Exception:
            logger.exception('登录出错')
