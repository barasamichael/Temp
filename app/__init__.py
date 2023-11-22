import flask
import flask_sqlalchemy
import flask_bootstrap
import flask_moment
import flask_cors
import flask_jwt_extended
from flask_login import LoginManager
from config import config

#set endpoint for the login page
login_manager = LoginManager()
login_manager.login_view = 'main.login'

db = flask_sqlalchemy.SQLAlchemy()
moment = flask_moment.Moment()
bootstrap = flask_bootstrap.Bootstrap()
cors = flask_cors.CORS()
jwt = flask_jwt_extended.JWTManager()

def create_app(config_name):
    """
    Application initialization.
    Takes as an argument one of the configuration classes defined in config.py
    """

    app = flask.Flask(__name__)
    app.config.from_object(config[config_name])

    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    cors.init_app(app)
    jwt.init_app(app)

    if app.config['SSL_REDIRECT']:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .authentication import authentication as authentication_blueprint
    app.register_blueprint(authentication_blueprint, 
            url_prefix = "/api/authentication")
    
    from .registration import registration as registration_blueprint
    app.register_blueprint(registration_blueprint, 
            url_prefix = "/api/registration")
    
    from .profiles import profiles as profiles_blueprint
    app.register_blueprint(profiles_blueprint, url_prefix = "/api/accounts")
    
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix = "/api")
    
    from .analytics import analytics as analytics_blueprint
    app.register_blueprint(analytics_blueprint, url_prefix = "/api/analytics")
    
    from .administration import administration as administration_blueprint
    app.register_blueprint(administration_blueprint, 
            url_prefix = "/api/administration")
    
    return app
