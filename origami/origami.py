from flask import Flask, request as user_req
from flask_cors import CORS, cross_origin
import magic
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from origami.utils import validate_token, parse_target
from origami import constants, exceptions, utils


class OrigamiPipeline(object):
    """ Implements pipeline functions for Origami
    Handles various pipeline functions such as fetching and saving data from and
    to cache.
    """
    def __init__(self):
        pass

    def cache_image_file(self):
        pass


class OrigamiInputs(OrigamiPipeline):
    """ Origami input functions
    Class implementing input functions for Origami, this class will be inherited
    by main Origami class.
    """
    def __init__(self):
        pass

    def get_text_array(self):
        """
        Extract text input from the request form.
        """
        text_inputs = []
        i = 0
        try:
            # TODO: Convert this to getlist to directly get the list of inputs
            while True:
                text_inputs.append(
                    user_req.form.get('input-text-{}'.format(i), type=str))
                i += 1
        except ValueError:
            pass
        if text_inputs:
            return text_inputs
        else:
            raise exceptions.InvalidRequestParameterGet(
                "No valid input text fields in the request")

    def get_image_array(self, mode=constants.INPUT_IMAGE_ARRAY_FILEPATH_MODE):
        """
        Extract image input from the request files.

        Args:
            mode: mode in which you are expecting the result
                file_path -> cache Image locally and return path
                numpy_array ->
        """
        image_inputs = []
        i = 0
        try:
            while True:
                image_inputs.append(user_req.files['input-image-{}'.format(i)])
                i += 1
        except Exception as e:
            if not image_inputs:
                raise exceptions.InvalidRequestParameterGet(
                    "No valid input image fields in the request")

        if mode == constants.INPUT_IMAGE_ARRAY_FILEPATH_MODE:
            return self.cache_image_file(image_inputs)

        elif mode == constants.INPUT_IMAGE_ARRAY_NPARRAY_MODE:
            return utils.get_image_as_numpy_arr(image_inputs)
        else:
            raise exceptions.InputHandlerException(
                "No valid mode provided when requesting user image input")


class OrigamiOutputs(object):
    def __init__(self):
        pass


class Origami(OrigamiInputs, OrigamiOutputs):
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

    def crossdomain(*args, **kwargs):
        """
        Implements cross-domain access for origami wrapped function.
        This is useful when the demo is deployed on some external server
        whose domain does not match with the origami.
        """
        return cross_origin
