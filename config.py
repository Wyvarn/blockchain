"""
Configurations for Flask application. This will be used to configure a flask application. Either a production,
development, testing or unix configuration can be used for this application. A dictionary is exported with the keys as
the configurations and the values as the instances of the configuration. A Config abstract base class is used to
configure the application
"""
import os
from abc import ABCMeta

from click import echo, style

basedir = os.path.abspath(os.path.dirname(__file__))
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# if the .env file exists, set the environment variables from the file
if os.path.exists(".env"):
    echo(style(text="Importing environment variables", fg="green", bold=True))
    for line in open(".env"):
        var = line.strip().split("=")
        if len(var) == 2:
            os.environ[var[0]] = var[1]


class Config(metaclass=ABCMeta):
    """
    Default configuration for application. This is abstract and thus will not be used when configuring the application.
    the class variables will be inherited by subclass configurations and either they will be used as is of there will be
    overrides
    :cvar SECRET_KEY
    :cvar ROOT_DIRECTORY
    :cvar CSRF_ENABLED
    :cvar CSRF_SESSION_KEY
    """

    __abstract__ = True

    SECRET_KEY = os.environ.get("SECRET_KEY", "blockchain")
    ROOT_DIRECTORY = APP_ROOT
    CSRF_ENABLED = True
    CSRF_SESSION_KEY = os.environ.get("CSRF_SESSION_KEY")

    @staticmethod
    def init_app(app):
        """Initialize the current application"""
        pass


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    DEBUG = True


class TestingConfig(Config):
    """
    Testing configurations
    """
    TESTING = True
    WTF_CSRF_ENABLED = False
    CSRF_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(Config):
    """
    Production configuration
    """
    TESTING = False
    DEBUG = False


config = {
    "develop": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}
