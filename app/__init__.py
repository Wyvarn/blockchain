import logging
from flask import Flask
from config import config
import jinja2

logger = logging.getLogger("BlockchainLogger")


class BlockApp(Flask):
    """
    Custom application class subclassing Flask application. This is to ensure more modularity in
     terms of static files and templates. This way a module will have its own templates and the
      root template folder will be more modularized and easier to manage
    """

    def __init__(self):
        """
        jinja_loader object (a FileSystemLoader pointing to the global templates folder) is
        being replaced with a ChoiceLoader object that will first search the normal
        FileSystemLoader and then check a PrefixLoader that we create
        """
        Flask.__init__(self, __name__, static_folder="static", template_folder="templates")
        self.jinja_loader = jinja2.ChoiceLoader([
            self.jinja_loader,
            jinja2.PrefixLoader({}, delimiter=".")
        ])

    def create_global_jinja_loader(self):
        """
        Overriding to return the loader set up in __init__
        :return: jinja_loader
        """
        return self.jinja_loader

    def register_blueprint(self, blueprint, **options):
        """
        Overriding to add the blueprints names to the prefix loader's mapping
        :param blueprint:
        :param options:
        """
        Flask.register_blueprint(self, blueprint, **options)
        self.jinja_loader.loaders[1].mapping[blueprint.name] = blueprint.jinja_loader


def create_app(config_name):
    """
    Creates an instance of the application by passing in the configuration name. The config name is either develop,
    production or testing
    :param config_name: Configuration to use for this application instance
    :type config_name str
    :return: flask application instance
    :rtype: Flask
    """

    app = BlockApp()

    # configure the application from the config name provided
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # register blueprints
    register_blueprints(app)

    # this will reduce the load time for templates and increase the application performance
    app.jinja_env.cache = {}

    return app


def register_blueprints(application):
    """
    Registers application blueprints
    :param application: Current flask application
    """
    from app.mod_blockchain import block

    application.register_blueprint(block)
