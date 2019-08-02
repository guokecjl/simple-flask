# coding: utf-8

import json

from flask import Flask, make_response
from flask_compress import Compress

import config
from router import register_urls

settings = {
    "import_name": config.ROOT_DIR,
    "static_folder": config.FRONT_DIR,
    "template_folder": config.FRONT_DIR,
    "static_url_path": '/static'
}

app = Flask(**settings)
if config.DEBUG:
    from flask_cors import CORS
    CORS(app, supports_credentials=True)


@app.errorhandler(422)
def handler_error(err):
    if config.DEBUG:
        print(err.data.get("messages", ["Invalid request."]))
    write_data = {
        "status": 0,
        "err_msg": '缺少必要的参数或者数据格式有误',
        "data": {},
        "err_code": 1201
    }
    response = make_response(json.dumps(write_data))
    response.headers["Content-type"] = "application/json"
    response.headers["status"] = 200
    return response


def prepare():
    app.config.from_object(config)

    Compress().init_app(app)
    register_urls(app)


if __name__ == "__main__":
    prepare()
    # import os
    # os.system('gunicorn -w4 -b{}:{} start:app'.format(config.HOST, config.PORT))
    app.run(host=config.HOST, port=config.PORT)
