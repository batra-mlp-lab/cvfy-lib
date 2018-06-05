from flask import Flask, request as user_req, jsonify
from flask_cors import CORS, cross_origin
import requests
import re
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from origami import constants, exceptions, utils


class OrigamiRequester(object):
    def __init__(self):
        pass

    def reqeust_origami_server(self, payload):
        """
        Makes a POST request to the origami server to send the payload, this
        can be used to send data to user via socket. First origami-lib makes
        request to Origami server providing the socket Id of the user which in
        turn inject the data to user browser provided in the data field of the
        payload.

        Args:
            payload: Python dict which is to be sent to the origami server
                The format of the payload is:
                payload = {
                    "socketId": userSocketID,
                    "[dataType]": data
                }

                where dataType can be one of the following.
                data, terminalData

        Returns:
            response_text:
                Response text returned from the request made.

        Raises:
            BadRequestException:
                400 when requesting
            NotFoundRequestException:
                404 when requesting
            InternalServerErrorException:
                500 when requesting
            OrigamiRequesterException:
                Some other error code when requesting
        """
        try:
            target_url = self._get_origami_server_target_url()
        except Exception as e:
            raise exceptions.RequesterNoTargetUrlException(
                "No target url retriver function _get_origami_server_target_url\
                found")

        # Request the origami server
        try:
            resp = requests.post(
                target_url,
                headers=constants.REQUESTS_JSON_HEADERS,
                data=payload)
        except Exception as e:
            raise exceptions.OrigamiRequesterException(
                "Connection error when requesting origami server")

        # Check the response object
        if resp.status_code == 400:
            raise exceptions.BadRequestException(
                "Bad Request: 400 when sending data to origami server")
        elif resp.status_code == 404:
            raise exceptions.NotFoundRequestException(
                "Not Found: 404 when sending data to origami server")
        elif resp.status_code == 500:
            raise exceptions.InternalServerErrorException(
                "Internal Server Error: 500 when requesting origami server")
        elif resp.status_code == 200:
            return resp.text
        else:
            raise exceptions.OrigamiRequesterException(
                "Connection error when requesting origami server")


class OrigamiPipeline(object):
    """ Implements pipeline functions for Origami
    Handles various pipeline functions such as fetching and saving data from
    and to cache.
    """

    def __init__(self):
        pass

    def cache_image_file(self):
        pass


class OrigamiInputs(OrigamiPipeline):
    """ Origami input functions
    Class implementing input functions for Origami, this class will be
    inherited by main Origami class.
    """

    def __init__(self):
        pass

    def get_text_array(self):
        """
        Extract text input from the request form.

        Returns:
            text_inputs: Input text array provided by user in the request.

        Raises:
            InvalidRequestParameterGet: Not a valid parameter requested from
                the users request to origami.
        """
        text_inputs = []
        i = 0
        # TODO: Convert this to getlist to directly get the list of inputs
        while True:
            input_text = user_req.form.get('input-text-{}'.format(i), type=str)
            if input_text:
                text_inputs.append(input_text)
            else:
                break
            i += 1

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

        Returns:
            ImageArr: array of Images either in the numpy array format or
                the path of the image which is cached locally.

        Raises:
            InputHandlerException: Exception that the input provided by user in
                the request is not Valid, which is some image is expected and
                none provided.
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


class OrigamiOutputs(OrigamiRequester):
    """ Origami output functionalities
    This class implements all the output functions for Origami.

    Attributes:
        response: response variable storing response to be sent to client
            if API access is enabled using the provided decorator.
    """
    response = list(constants.DEFAULT_ORIGAMI_RESPONSE_TEMPLATE)

    def __init__(self):
        pass

    def _clear_response(self):
        """
        Clears the response variable to have the default template
        response string

        Returns:
            response: string which was in self.response before clearing
                it up.
        """
        response = jsonify(self.response)
        # Make a copy of the constant origami response template in self.response
        self.response = list(constants.DEFAULT_ORIGAMI_RESPONSE_TEMPLATE)
        return response

    def _send_api_response(self, payload):
        """
        Set the response for user request as a json object of payload

        Args:
            payload: payload(python dict) to be sent to the user

        Returns:
            Jsonified json response object.
        """
        self.response.append(payload)
        return self.response

    def origami_api(self, view_func):
        """
        Decorator to decorate the user defined main function to
        send user an API response at the end of the request.

        Args:
            view_func: Function that this function wraps to make
                things work.

        Returns:
            Wrapper fuction that calls the view_func to do its work
            and then returns the response back to user.
        """

        def _wrapper():
            view_func()
            response = self._clear_response()
            return response

        return _wrapper

    def _origmai_send_data(self, data, dataType):
        """
        Core function which sends output to either the origami server or the
        user as response to request

        Args:
            data: list or tuple of string to be sent.
            dataType: Key for data in payload python dict
                can be either of `data` or `terminalData`

        Returns:
            resp: Response we sent to user as API response or response from
                the origami server.
        """
        resp = None
        socketId = user_req.form.get(constants.REQUEST_SOCKET_ID_KEY, type=str)
        # Check if a valid socketId is provided in the request
        # else consider it as an API request.

        if socketId:
            # Check if the socket-id is there is the request form.
            payload = {"socketId": socketId, dataType: data}
            resp = self.request_origami_server(payload)

        else:
            # TODO: Discuss the strucutre of API response payload.
            payload = {"data": data}
            resp = self._send_api_response(payload)

        return resp

    # Data sending functions

    def send_text_array(self, data, dataType=constants.DEFAULT_DATA_TYPE_KEY):
        """
        Send text data array to origami_server with the users socket ID

        Args:
            data: list or tuple of string to be sent.
            dataType: Key for data in payload python dict
                can be either of data or terminalData

        Returns:
            resp: Response text we got back from the origami server
            corresponding to the request we made.

        Raises:
            MismatchTypeException: Type of the data provided to function is not
                what we expected.
        """

        # TODO: make dataType more explicit here use different types for images
        # and graphs too so they can be handled properly via origami.

        if not isinstance(data, (list, tuple)):
            raise exceptions.MismatchTypeException(
                "send_text_array can only accept an array or a tuple")

        if not all(utils.check_if_string(element) for element in data):
            raise exceptions.MismatchTypeException(
                "send_text_array expects a list or tuple of string")

        resp = self._origmai_send_data(data, dataType)
        return resp

    def send_graph_array(self, data):
        """
        Send text data array to origami_server with the users socket ID

        Args:
            data: list or tuple of list/tuple to be sent.

        Returns:
            resp: Response text we got back from the origami server
            corresponding to the request we made.

        Raises:
            MismatchTypeException: Type of the data provided to function is not
                what we expected.
        """

        if not isinstance(data, (list, tuple)):
            raise exceptions.MismatchTypeException(
                "send_graph_array can only accept an array or a tuple.")

        if not all(isinstance(element, (list, tuple)) for element in data):
            raise exceptions.MismatchTypeException(
                "send_graph_array expects a list/tuple of list/tuple")

        resp = self._origmai_send_data(data, constants.DEFAULT_DATA_TYPE_KEY)
        return resp

    def send_text_array_to_terminal(self, data):
        """
        Send the array/tuple provided as argument to the origami server
        as a terminal data.

        Args:
            data: array/tuple of strings to be sent.

        Returns:
            resp: response got from sending the data.
        """
        resp = self.send_text_array(data, constants.TERMINAL_DATA_TYPE_KEY)
        return resp

    def send_image_array(self,
                         data,
                         mode=constants.INPUT_IMAGE_ARRAY_FILEPATH_MODE):
        """
        Send image array as base64 encoded images list.

        Args:
            data: list/tuple of either image path or numpy array
            mode: mode in which to process the data

        Returns:
            resp: response got from sending the data.

        Raises:
            MismatchTypeException: data is not of list/tuple type
        """
        if not isinstance(data, (list, tuple)):
            raise exceptions.MismatchTypeException(
                "send_image_array can only accept a list or a tuple.")

        image_arr = []

        # Mode -> file_path
        if mode == constants.INPUT_IMAGE_ARRAY_FILEPATH_MODE:
            for file_path in data:
                img_src = utils.get_base64_image_from_file(file_path)
                image_arr.append(img_src)

        # Mode -> NP Array
        elif mode == constants.INPUT_IMAGE_ARRAY_NPARRAY_MODE:
            for np_image_arr in data:
                img_src = utils.get_base64_image_from_nparr(np_image_arr)
                image_arr.append(img_src)

        else:
            raise exceptions.OutputHandlerException(
                "Not a valid mode({0}) provided when encoding image for sending",
                mode)

        resp = self._origmai_send_data(image_arr,
                                       constants.DEFAULT_DATA_TYPE_KEY)
        return resp


class Origami(OrigamiInputs, OrigamiOutputs):
    """ Origami class to declare the main app

    This class initializes the app and provides methods to interact with
    the web interface.

    Attributes:
        name: Application name.
        origami_server_base: URL for origami server running.

        server: Flask server for origami
        cors: CORS for flask server running
    """

    def __init__(self, name, server_base=constants.ORIGAMI_SERVER_BASE_URL):
        """
        Inits class with provided arguments
        """

        self.app_name = name
        self.origami_server_base = server_base
        # self.token = validate_token(token)
        # self.target = parse_target(token)

        self.server = Flask(__name__)
        self.cors = CORS(self.server)

    def _get_origami_server_target_url(self):
        """
        Returns orgiami server target url for flask server to use for injecting
        output.

        Returns:
            target_url: Origami server target url

        Raises:
            MismatchTypeException: Error occured when correct type of token is
                not supplied.
        """
        try:
            assert isinstance(self.origami_server_base, str)
        except AssertionError:
            raise exceptions.MismatchTypeException(
                "Server base url type mismatch: string expected given %s"
                .format(type(self.origami_server_base)))

        target_protocol = constants.HTTPS_ENDPOINT
        if re.search(constants.LOCAL_TARGET_REGEXP, self.origami_server_base):
            target_protocol = constants.HTTP_ENDPOINT

        target_url = "{0}{1}{2}".format(target_protocol,
                                        self.origami_server_base,
                                        constants.ORIGAMI_SERVER_INJECTION_PATH)
        return target_url

    def listen(self, route=constants.ORIGAMI_DEFAULT_EVENT_ROUTE):
        """ Listen decorator wrapper for origami

        This function acts as a wrapper around the Flasks app.route() decorator
        By default we are restricting this to only POST methods.

        Args:
            route: route to be uesd by origami web interface for interaction
        """
        return self.server.route(
            route, methods=[
                "GET",
                "POST",
            ])

    def run(self):
        """
        Starts the flask server over Tornados WSGI Container interface

        Raises:
            OrigamiServerException: Exception when the port we are trying to
                bind to is already in use.
        """
        try:
            port = constants.DEFAULT_PORT
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
