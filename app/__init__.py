import flask
import flask_moment
import flask_sqlalchemy
from flask_login import LoginManager
from config import config

#set endpoint for the login page
login_manager = LoginManager()
login_manager.login_view = 'authentication.login'

moment = flask_moment.Moment()
db = flask_sqlalchemy.SQLAlchemy()

def create_app(config_name):
    """
    Application initialization.
    Takes as an argument one of the configuration classes defined in config.py
    """

    app = flask.Flask(__name__)
    app.config.from_object(config[config_name])

    moment.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)

    if app.config['SSL_REDIRECT']:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .authentication import authentication as authentication_blueprint
    app.register_blueprint(authentication_blueprint)
    
    from .registration import registration as registration_blueprint
    app.register_blueprint(registration_blueprint)
    
    from .account import account as account_blueprint
    app.register_blueprint(account_blueprint)
    
    return app
