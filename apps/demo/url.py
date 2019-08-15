# coding: utf-8

from .hello import HelloWorldHandler

urls = [
    ('/demo/hello', HelloWorldHandler.as_view('hellow'))
]