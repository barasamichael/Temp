import flask
from flask_login import login_user, logout_user, login_required
from . import main
from ..models import User

@main.route('/')
def index():
    return flask.render_template('main/index.html')


@main.route('/about-us')
def about_us():
    return flask.render_template('main/about_us.html')


@main.route('/contact-us')
def contact_us():
    return flask.render_template('main/contact_us.html')


@main.route('/how-it-works')
def how_it_works():
    return flask.render_template('main/how_it_works.html')


@main.route('/terms-and-conditions')
def terms_and_conditions():
    return flask.render_template('main/terms_and_conditions.html')


@main.route('/faq')
def faq():
    return flask.render_template('main/faq.html')


@main.route('/privacy-policy')
def privacy_policy():
    return flask.render_template('main/privacy_policy.html')
