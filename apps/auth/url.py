# coding: utf-8

from .auth import IndexHandler

urls = [
    ("/", IndexHandler.as_view("index")),
    ("/<string:path>", IndexHandler.as_view("redirect_index")),
    ("/<string:path>/<string:other_path>", IndexHandler.as_view(
        "redirect_index2"))
]