import flask
import json
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, logout_user, login_required, current_user
from . import authentication
from .. import db
from .forms import LoginForm
from ..models import User


@authentication.route('/logout')
@login_required
def logout():
    # Maintain email address of current user
    email_address = current_user.id

    # Logout user
    logout_user()

    # Delete entry from storage
    User.query.filter(User.id == email_address).delete()
    db.session.commit()

    # Indicate user is logged out
    flask.flash("You've been logged out.")

    # Redirect user to login page
    return flask.redirect(flask.url_for('authentication.login'))


@authentication.route('/login', methods = ['GET', 'POST'])
def login():
    # Check whether the user logged in
    if current_user.is_authenticated:
            next = flask.url_for('account.dashboard')
            return flask.redirect(next)

    return flask.render_template('authentication/login.html')


@authentication.route('/successful', methods = ["POST"])
def successful():
    form = flask.request.form
    token = form.get('token')
    details = json.loads(form.get('details'))

    # Initialize User
    user = User()
    user.id = details.get("emailAddress")
    user.token = token
    user.userId = details.get("userId")
    user.imageUrl = details.get("imageUrl")
    user.avatarUrl = details.get("avatarUrl")

    # Save user to the database
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        pass

    # Login user
    login_user(user)

    # Redirect user to dashboard
    return flask.redirect(flask.url_for("account.dashboard"))
