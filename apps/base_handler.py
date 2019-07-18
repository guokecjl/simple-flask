# coding: utf-8

import json
import functools

from flask import make_response, request
from flask.views import MethodView

from lib.logger import logger
# from database_clients.redis_cli import redis_cli
# from database_clients.mongo_cli import g4tect_client, gt_account_client,\
#     gt_data_center_client
# from database_clients.mysql_cli import mysql_engine
from config import DEBUG, LOGIN_URL


class RunException(BaseException):
    """
    异常类
    """
    def __init__(self, status, error_msg):
        self.status = status
        self.error_msg = error_msg


class BaseHandler(MethodView):
    def __init__(self, **kwargs):
        super(BaseHandler, self).__init__()
        self.logger = logger
        # self.redis_cli = redis_cli
        # self.g4_db = g4tect_client
        # self.account_db = gt_account_client
        # self.data_db = gt_data_center_client
        # self.mysql = mysql_engine

        self.power = []

    @classmethod
    def options(cls, *args, **kwargs):
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = "*"
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers["Content-type"] = "application/json"
        response.headers[
            'Access-Control-Allow-Headers'] = \
            'origin, x-csrftoken, content-type, accept, x-requested-with'
        response.headers['Access-Control-Allow-Headers'] = \
            'origin, x-csrftoken, Content-Type, accept, responseType'
        return response

    @staticmethod
    def write_response(data=None, status=1, err_msg="", err_code=0,
                       http_status=200):
        _data = {
            "status": int(status),
            "err_msg": err_msg,
            "err_code": err_code,
            "data": data
        }
        response = make_response(json.dumps(_data))
        response.headers["Content-type"] = "application/json"
        response.headers["status"] = http_status

        return response

    # @property
    # def admin_id(self):
    #     return self.session.get('_id', None)
    #
    # @property
    # def session_id(self):
    #     session_id = request.cookies.get('god_session_id', None)
    #     return session_id
    #
    # @property
    # def session(self):
    #     if DEBUG:
    #         user = self.data_db.AdminUser.find_one({"_id": DEFAULT_USER})
    #         return user
    #
    #     session_id = self.session_id
    #     if not session_id:
    #         return None
    #     try:
    #         user_id = self.redis_cli.get(session_id)
    #         if not user_id:
    #             return None
    #         user_id = user_id.decode()
    #         user = self.data_db.AdminUser.find_one({"_id": user_id})
    #         if not user:
    #             return None
    #         return user
    #     except Exception:
    #         logger.exception('获取session出错')
    #         return None
    #
    # def clear_session(self):
    #     try:
    #         if self.session_id:
    #             self.redis_cli.delete(self.session_id)
    #     except Exception:
    #         logger.exception('清除session出错')


def login_required(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.session:
            return '<script>window.location.href = "{}"</script>'.format(
                LOGIN_URL)
        return func(self)
    return wrapper


def check_power(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if not hasattr(self, 'group') or not hasattr(self, 'operation') or \
                not hasattr(self, 'power_list'):
            return self.write_response(status=0, err_msg="权限不足", err_code=1302)

        power = self.session.get("power", {})
        if not power.get(self.group, {}).get(self.operation, {}):
            return self.write_response(status=0, err_msg="权限不足", err_code=1302)
        self.power = power[self.group][self.operation]

        if not (set(self.power) & set(self.power_list)):
            return self.write_response(status=0, err_msg="权限不足", err_code=1302)
        return func(self)
    return wrapper
