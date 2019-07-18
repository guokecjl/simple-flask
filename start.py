# coding: utf-8

import json

from flask import Flask
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
    """
    处理某种错误码的错误
    """
    pass


def prepare():
    app.config.from_object(config)

    Compress().init_app(app)
    register_urls(app)


if __name__ == "__main__":
    prepare()
    app.run(host=config.HOST, port=config.PORT)
    # import os
    # os.system('gunicorn -w4 -b{}:{} start:app'.format(config.HOST, config.PORT))
