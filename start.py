# coding: utf-8

import json

from flask import Flask, render_template
from flask_compress import Compress

import config
from router import register_urls

from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

settings = {
    "import_name": config.ROOT_DIR,
    "static_folder": config.FRONT_DIR,
    "template_folder": config.FRONT_DIR,
    "static_url_path": '/static'
}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
if config.DEBUG:
    from flask_cors import CORS
    CORS(app, supports_credentials=True)

bootstrap = Bootstrap(app)
moment = Moment(app)


class NameForm(FlaskForm):
    name = StringField('Please input your account', validators=[DataRequired()])
    secret = StringField('Please input your secret', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/login', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('index.html', form=form, name=name)
    #return '<h1>Hello World!</h1>'


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
    app.run(debug=True)
    #app.run(host=config.HOST, port=config.PORT)
    # import os
    # os.system('gunicorn -w4 -b{}:{} start:app'.format(config.HOST, config.PORT))
