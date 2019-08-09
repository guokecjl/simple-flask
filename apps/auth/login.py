# coding: utf-8

from webargs.flaskparser import use_args
from marshmallow import fields

from apps.base_handler import BaseHandler
from lib.logger import logger


class LoginHandler(BaseHandler):

    args_format = {
        'email': fields.Str(required=True, validate=bool),
        'password': fields.Str(required=True, validate=bool)

    }

    @use_args(args_format)
    def post(self, args):
        try:
            email, pwd = args['email'], args['password']
        except Exception:
            logger.exception('登录出错')
