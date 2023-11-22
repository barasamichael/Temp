import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    BASE_DIRECTORY = basedir
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
            'The City Under the Sun'

    SSL_REDIRECT = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    ORGANIZATION_NAME = os.environ.get('ORGANISATION_NAME') or\
            'Danson and Serah Kiundi Foundation'
    API_SERVER_INDEX = "http://127.0.0.1:5001/"

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') \
            or 'sqlite:///' + os.path.join(basedir, 'data-dev-sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite://'
    WTF_CRF_ENABLED = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') \
            or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # Email errors to the administrators
        import logging
        from logging.handlers import SMTPHandler

        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure()

        mail_handler = SMTPHandler(
                mailhost = (cls.MAIL_SERVER, cls.MAIL_PORT),
                fromaddr = cls.COMMUNICATIONS_EMAIL,
                toaddrs = [cls.ADMINISTRATOR_EMAIL],
                subject = 'Application Error',
                credentials = credentials,
                secure = secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


class HerokuConfig(ProductionConfig):
    pass


class DockerConfig(ProductionConfig):
    pass


class UnixConfig(ProductionConfig):
    pass


config = {
        'development' : DevelopmentConfig,
        'testing' : TestingConfig,
        'production' : ProductionConfig,
        'heroku' : HerokuConfig,
        'docker' : DockerConfig,
        'unix' : UnixConfig,
        'default' : DevelopmentConfig
        }
