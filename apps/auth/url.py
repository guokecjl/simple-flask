# coding: utf-8

from .index import IndexHandler
from .login import LoginHandler
from .register import RegisterHandler

urls = [
    ("/", IndexHandler.as_view("index")),
    ("/<string:path>", IndexHandler.as_view("redirect_index")),
    ("/<string:path>/<string:other_path>", IndexHandler.as_view(
        "redirect_index2")),

    ('/auth/login', LoginHandler.as_view('user_login')),
    ('/auth/register', RegisterHandler.as_view('user_register'))
]