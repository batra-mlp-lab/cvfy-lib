class OrigamiException(Exception):
    """
    Base class for all exceptions thrown by origami.
    """
    STATUS_CODE = 500

    def __init__(self, message=''):
        super().__init__("[{0}] => {1}".format(self.STATUS_CODE, message))


class MismatchTypeException(OrigamiException):
    """
    These exceptions are cause during mismatched types.
    """
    STATUS_CODE = 100


class InputHandlerException(OrigamiException):
    """
    Exception while handling user request input.
    """
    STATUS_CODE = 300


class InvalidRequestParameterGet(OrigamiException):
    """
    These exceptions are caused when reqeusting invalid input parameters from
    user request.
    """
    STATUS_CODE = 301


class OrigamiRequesterException(OrigamiException):
    """
    Some other status code when requesting resource using OrigmaiRequester
    """
    STATUS_CODE = 400


class BadRequestException(OrigamiException):
    """
    400 when making a request using OrigamiRequester.
    """
    STATUS_CODE = 401


class NotFoundRequestException(OrigamiException):
    """
    404 when requesting a resource using OrigamiRequester
    """
    STATUS_CODE = 402


class InternalServerErrorException(OrigamiException):
    """
    500 when requesting the resource using OrigamiRequester
    """
    STATUS_CODE = 403


class InvalidTokenException(OrigamiException):
    """
    These exceptions are caused by providing invalid token to origami
    while registering app.
    """
    STATUS_CODE = 500


class OrigamiServerException(OrigamiException):
    """
    These exceptions are caused during error during server running.
    """
    STATUS_CODE = 501
