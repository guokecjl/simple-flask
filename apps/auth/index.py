# coding: utf-8

from flask import render_template

from apps.base_handler import BaseHandler
from lib.logger import logger


class IndexHandler(BaseHandler):

    def get(self, *args, **kwargs):
        try:
            return self.write_response(status=0, err_code=567,
                                       err_msg='接口调试成功')
        except Exception:
            logger.exception('加载静态文件出错')
            return self.write_response(status=0, err_code=1400,
                                       err_msg='获取前段资源出错')
