# coding: utf-8

from webargs.flaskparser import use_args
from marshmallow import fields

from apps.base_handler import BaseHandler
from lib.logger import logger


class RegisterHandler(BaseHandler):

    args_format = {
        'user_name': fields.Str(required=True, validate=bool),
        'password': fields.Str(required=True, validate=bool),
        're_password': fields.Str(required=True, validate=bool)
    }

    @use_args(args_format)
    def post(self, args):
        try:
            user_name = args['user_name']
            password = args['password']
            re_password = args['re_password']
            if password != re_password:
                return self.write_response(status=0, err_msg='两次密码不一致',
                                           err_code=1202)

            user_info = self.account.UserProfile.find_one({
                '_id': user_name
            })
            if user_info:
                return self.write_response(status=0, err_code=1202,
                                           err_msg='该用户已经存在')

            insert_data = {
                '_id': user_name,
                'password': '',
                'create_time': ''
            }
            return self.write_response({})
        except Exception:
            logger.exception('注册出错')
            return self.write_response(status=0, err_msg='注册出错',
                                       err_code=1400)
