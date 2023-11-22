from flask_login import AnonymousUserMixin, UserMixin
from . import db, login_manager


class Permission:
    VISIT = 1
    MEMBER = 2
    MODERATE = 4
    ADMIN = 8


@login_manager.user_loader
def load_user(email_address):
    """
    Returns User object containing info about the logged-in user
    """
    return User.query.get(email_address)


class Anonymous_User(AnonymousUserMixin): ...


login_manager.anonymous_user = Anonymous_User


class User(db.Model, UserMixin):
    id = db.Column(db.String(120), primary_key = True)
    token = db.Column(db.String(120))
    userId = db.Column(db.Integer)
    imageUrl = db.Column(db.String(255))
