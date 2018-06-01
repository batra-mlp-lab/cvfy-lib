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
    STATUS_CODE = 501


class OrigamiServerException(OrigamiException):
    """
    These exceptions are cause during mismatched types.
    """
    STATUS_CODE = 502


class InvalidTokenException(OrigamiException):
    """
    These exceptions are caused by providing invalid token to origami
    while registering app.
    """
    STATUS_CODE = 401
