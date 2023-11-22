import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
            'Seek knowledge even if you have to go as far as China'
    JWT_SECRET_KEY = os.environ.get('SECRET_KEY') or \
            "Behold here I come. And in ruins they shall lie."
    JWT_ACCESS_TOKEN_EXPIRES = 7200

    SSL_REDIRECT = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SLOW_DB_QUERY_TIME = 0.5

    ORGANIZATION_NAME = os.environ.get('ORGANISATION_NAME') or\
            'OBRS'

    USER_IMAGES_UPLOAD_PATH = os.path.join(basedir +
            '/app/static/images/profiles/')
    BOOK_IMAGES_UPLOAD_PATH = os.path.join(basedir +
            '/app/static/images/books/')
    UPLOAD_EXTENSIONS = ['.jpg', '.gif', '.jpeg', '.png']

    ADMINISTRATOR_EMAIL = os.environ.get('ADMINISTRATOR_EMAIL') or\
            'administrator@obrs.co.ke'


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
