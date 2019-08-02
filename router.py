# coding: utf-8

import apps.demo.url
import apps.auth.url

sub_routes = [
    ('', apps.demo.url.urls),
    ('', apps.auth.url.urls)
]

def register_urls(app):
    for pre_url, _routes in sub_routes:
        for suf_url, handler in _routes:
            app.add_url_rule(r"{}{}".format(pre_url, suf_url), view_func=handler)
