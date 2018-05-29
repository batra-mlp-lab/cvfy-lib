import cv2
import io
import numpy as np

from origami import exceptions, constants


def validate_token(token):
    """ Validate the provided token

    Check if the provided token in argument is valid for app

    Args:
        token: Token string which is to be validated

    Returns:
        token: Token if validated else an exception is raised

    Raises:
        MismatchTypeException: Error occured when correct type of token is not
             supplied.
        InvaidTokenException: Raised when token to be validated is invalid
    """
    try:
        assert isinstance(token, str)
    except AssertionError:
        raise exceptions.MismatchTypeException(
            "TOKEN type mismatch: string expected given %s".format(type(token)))
    try:
        if (token.split(':')[0] in constants.DEMO_DEPLOYMENT_TYPE):
            assert int(token.split(':')[3])
            assert int(token.split(':')[4])
        else:
            raise AssertionError
    except AssertionError:
        raise exceptions.InvalidTokenException(
            "TOKEN invalid: Required format %s".format(constants.TOKEN_FORMAT))
    return token


def parse_target(token):
    """ Parses target of the application from the applicaiton token

    This function assumes that the token you are providing has been validated
    earlier using `validate_token` function, so it does not attempt to check
    validity.

    Args:
        token: Token to extract the target from

    Returns:
        target: Target of the application
            either gh or nongh.

    Raises:
        InvalidTokenException: The token provided is invalid, it only checks it
            corresponding to target
    """
    if (token.split(':')[0] == 'gh'):
        target = 'local'
    elif (token.split(':')[0] == 'nongh'):
        target = 'remote'
    else:
        raise exceptions.InvalidTokenException(
            "TOKEN invalid: Required format %s".format(constants.TOKEN_FORMAT))

    return target


def get_image_as_numpy_arr(image_files_arr):
    """ Takes an array of image files and returns numpy array for the same

    This function is a helper function which takes in image files from users
    request and returns the corresponding numpy array for images.

    Args:
        image_files_arr: Array of image files from user request

    Returns:
        image_np_arr: Array of numpy image array corresponding to given
            image files.
    """
    images_np_arr = []

    for index, image_object in enumerate(image_files_arr):
        in_memory = io.BytesIO()
        image_object.save(in_memory)
        data = np.fromstring(in_memory.getvalue(), dtype=np.uint8)
        color_image_flag = 1
        image = cv2.imdecode(data, color_image_flag)

        images_np_arr.append(image)

    return images_np_arr
