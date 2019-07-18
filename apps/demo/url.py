# coding: utf-8

from .hello import HelloWorldHandler

urls = [
    ('/hello', HelloWorldHandler.as_view('hellow'))
]