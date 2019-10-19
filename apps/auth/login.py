# coding: utf-8

from webargs.flaskparser import use_args
from marshmallow import fields

from apps.base_handler import BaseHandler
from lib.logger import logger
from lib.tools import encrypt_password


class LoginHandler(BaseHandler):

    args_format = {
        'user_name': fields.Str(required=True, validate=bool),
        'password': fields.Str(required=True, validate=bool)
    }

    @use_args(args_format)
    def post(self, args):
        try:
            user_name, pwd = args['user_name'], args['password']
            # 查询用户名
            user_info = self.account.UserProfile.find_one({
                '_id': user_name
            })
            print(user_info)
            if user_info:
                if user_info['password'] == encrypt_password(pwd):
                    return self.write_response(status=0, err_code=200,
                                           data='登陆成功')
                else:
                    return self.write_response(status=0, err_code=1202,
                                               data='密码错误')
            else:
                return self.write_response(status=0, err_code=1202, err_msg='用户不存在', data=user_info)
        except Exception:
            logger.exception('登录出错')
