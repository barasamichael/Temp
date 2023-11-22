import flask
from flask_login import current_user, login_required, login_user
from . import registration
from ..models import User

@registration.route("/register_user", methods = ["GET"])
def register_user():
    return flask.render_template("registration/register_user.html")

@registration.route("/register_author", methods = ["GET"])
def register_author():
    return flask.render_template("registration/register_author.html")


@registration.route("/add_book", methods = ["GET"])
def add_book():
    return flask.render_template("registration/add_book.html")


@registration.route("/add_role", methods = ["GET"])
def add_role():
    return flask.render_template("registration/add_role.html")


@registration.route("/add_category", methods = ["GET"])
def add_category():
    return flask.render_template("registration/add_category.html")


@registration.route("/add_raffle", methods = ["GET"])
def add_raffle():
    return flask.render_template("registration/add_raffle.html")
