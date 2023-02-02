from util.date import get_date_of_expire
from config.env import SECRET_KEY_ENCODE
from config.vars import EXPIRATION_DATE_IN_DAYS
from jwt import encode, decode, exceptions
from flask import jsonify


def create_tocken(data: dict) -> bytes:
    """This function creates a tocken to validate and give access to the api

    Args:
        data (dict): This dictionary is the information you will use to create the token, usually username and password.

    Returns:
        bytes: Returns tocken as a byte type
    """

    # Calculate expiration date.
    expiration_date = get_date_of_expire(EXPIRATION_DATE_IN_DAYS)

    # Create the tocken with the encode function of jwt.
    tocken = encode(payload={**data, "exp": expiration_date},
                    key=SECRET_KEY_ENCODE, algorithm="HS256")
    # Returns the token as a byte type.
    return tocken.encode(encoding='UTF-8')


def validate_tocken(tocken: str, output=False):
    """This function validates whether the token is valid and may or may not return the information that was used to create the token.

    Args:
        tocken (str): Tocken as string type.
        output (bool, optional): Indicates if you want to obtain the tocken creation dictionary. Defaults to False.

    Returns:
        (Dic | Response | None): It can return the tocken dictionary, a response to the api in case of error or it can return nothing.
    """

    # Decifers the contents of the token if an error occurs compare the error obtained for replying to a special message as expired or invalid.
    try:
        # Get the answer from the tocken.
        output_validation = decode(
            tocken,  key=SECRET_KEY_ENCODE, algorithms=["HS256"])
        # In case output is required return output.
        if output:
            return output_validation
    except exceptions.DecodeError:
        # This response is obtained when the tocken is an invalid tocken, it returns a response as a json indicating the error.
        response = jsonify({"msg": "The tocken is invalid",  "msg web": "Hi, this api is in charge of serving some data and other materials for my web pages and projects like my portfolio, it hosts several types of methods like sending messages etc. In order to use this api is required the user and password this to generate a tocken that gives the authorization to the api.", })
        response.status_code = 401
        response.headers.set('Content-Type', 'application/json; charset=utf-8')
        return response
    except exceptions.ExpiredSignatureError:
        # This response is obtained when the tocken has expired, it returns a response as a json indicating the error.
        response = jsonify({"msg": "Your token has expired",  "msg web": "Hi, this api is in charge of serving some data and other materials for my web pages and projects like my portfolio, it hosts several types of methods like sending messages etc. In order to use this api is required the user and password this to generate a tocken that gives the authorization to the api.", })
        response.status_code = 401
        response.headers.set('Content-Type', 'application/json; charset=utf-8')
        return response
