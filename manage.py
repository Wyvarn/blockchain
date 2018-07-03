import better_exceptions
from flask_script import Manager, Shell, Server
from app import create_app, logger
import os

# create the application configuration
app = create_app(os.environ.get("FLASK_CONFIG", "default"))

PORT = 5000
manager = Manager(app)
server = Server(host="127.0.0.1", port=PORT)
public_server = Server(host="0.0.0.0", port=PORT)


def make_shell_context():
    """
    Makes a shell context
    :return dictionary object
    :rtype: dict
    """
    return dict(app=app)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("runserver", server)
manager.add_command("publicserver", public_server)


@manager.command
def test(cover=False):
    """Run the unit tests."""
    import coverage

    cov = coverage.coverage(branch=True, include="app/*")
    cov.start()

    if cover and not os.environ.get("FLASK_COVERAGE"):
        import sys

        os.environ["FLASK_COVERAGE"] = "1"
        os.execvp(sys.executable, [sys.executable] + sys.argv)

    import unittest

    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)
    if cover:
        cov.stop()
        cov.save()
        logger.debug("Coverage Summary:")

        cov.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, "coverage")

        # generate html report
        cov.html_report(directory=covdir)

        # generate xml report
        cov.xml_report()

        logger.debug(f"HTML version: file://{covdir}/index.html")
        logger.debug(f"XML version: file://{covdir}")
        cov.erase()


@manager.command
def profile(length=25, profile_dir=None):
    """
    This module provides a simple WSGI profiler middleware for finding
    bottlenecks in web application. It uses the profile or cProfile
    module to do the profiling and writes the stats to the stream provided

    see: http://werkzeug.pocoo.org/docs/0.9/contrib/profiler/
    """
    from werkzeug.contrib.profiler import ProfilerMiddleware

    app.config["PROFILE"] = True
    app.wsgi_app = ProfilerMiddleware(
        app.wsgi_app, restrictions=[length], profile_dir=profile_dir
    )
    app.run()


if __name__ == "__main__":
    manager.run()
