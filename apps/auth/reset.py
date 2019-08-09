# coding: utf-8

from webargs.flaskparser import use_args
from marshmallow import fields

from apps.base_handler import BaseHandler
from lib.logger import logger


class SendResetEmailHandler(BaseHandler):

    args_format = {
        'email': fields.Str(required=True, validate=bool)
    }

    @use_args(args_format)
    def post(self, args):
        try:
            email = args['email']
        except Exception:
            logger.exception('发送邮件出错')


class ResetPasswordHandler(BaseHandler):

    args_format = {
        'email': fields.Str(required=True, validate=bool),
        'key': fields.Str(required=True, validate=bool),
        'new_pwd': fields.Str(required=True, validate=bool)
    }

    @use_args(args_format)
    def post(self, args):
        try:
            email = args['email']
            key, new_pwd = args['key'], args['new_pwd']
        except Exception:
            logger.exception('重置密码出错')
