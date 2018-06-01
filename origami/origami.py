from flask import Flask
from flask_cors import CORS
import magic
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from origami.utils import validate_token, parse_target
from origami import constants, exceptions


class Origami(object):
    """ Origami class to declare the main app

    This class initializes the app and provides methods to interact with
    the web interface.

    Attributes:
        app_name: Application name.
        token: Origami token for the application.
        target: target of the interface CV/user deployment
    """

    def __init__(self, app_name, token):
        """
        Inits class with provided arguments
        """

        self.app_name = app_name
        self.token = validate_token(token)
        self.target = parse_target(token)

        self.server = Flask(__name__)
        self.cors = CORS(self.server)
        self.mime = magic.Magic(mime=True)

    def listen(self, route=constants.ORIGAMI_DEFAULT_EVENT_ROUTE):
        """ Listen decorator wrapper for origami

        This function acts as a wrapper around the Flasks app.route() decorator
        By default we are restricting this to only POST methods.

        Args:
            route: route to be uesd by origami web interface for interaction
        """
        return self.server.route(route, methods=["GET", "POST", ])

    def run(self):
        """
        Starts the flask server over Tornados WSGI Container interface

        Raises:
            OrigamiServerException: Exception when the port we are trying to
                bind to is already in use.
        """
        try:
            port = int(self.token.split(':')[4])
            http_server = HTTPServer(WSGIContainer(self.server))
            http_server.listen(port)
            print("Origami server running on port: {}".format(port))
            IOLoop.instance().start()
        except OSError:
            raise exceptions.OrigamiServerException(
                "ORIGAMI SERVER ERROR: Port {0} already in use.".format(port))
