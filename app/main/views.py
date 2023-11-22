import flask
import requests
import flask_login
from . import main

@main.route('/')
@main.route('/home')
@main.route('/homepage')
def index():
    return flask.render_template('main/index.html')


@main.route('/register')
def register():
    return flask.render_template('main/register.html')


@main.route('/login')
def login():
    return flask.render_template('main/login.html')


@main.route('/documentation')
def documentation():
    return flask.render_template('main/documentation.html')


@main.route('/dashboard')
def dashboard():
    return flask.render_template('main/dashboard.html')


@main.route('/upload')
def upload():
    return flask.render_template('main/upload_image.html')


@main.route('/open-raffle')
def open_raffle():
    return flask.render_template('main/open_raffle.html')


