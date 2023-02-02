from flask import Blueprint, jsonify, request
from util.tokens import create_tocken
from config.env import SECRET_ROOT_USERNAME, SECRET_ROOT_PASSWORD
from bcrypt import gensalt, hashpw, checkpw

auth_pages = Blueprint('auth_pages', __name__)


@auth_pages.route('/login', methods=['POST'])
def obtainAuthentication():
    """Request the correct username and password in order to generate a token and access the api content.

    Returns:
        (Response): Returns the message with the tocken if it is set, or a null if it is not set. 
    """
    try:
        # Get the json content to be sent to the api.
        data = request.get_json()

        # Separate contents as username or password
        username = data["username"]
        password = data["password"]
        # If the username and password are correct, then you can create a tocken and send it as a reply, if not then just send the message with the tocken set to null.
        if username == SECRET_ROOT_USERNAME and password == SECRET_ROOT_PASSWORD:
            # Create the tocken and convert it to a string type.
            tocken = create_tocken(data)
            tocken = tocken.decode('utf8', 'strict')
            # Message to send.
            response = jsonify(
                {"msg": "Tocken successfully created", "tocken": tocken})
            response.status_code = 200
            return response
        else:
            # Message to send.
            response = jsonify(
                {"msg": "Authentication failed", "tocken": None})
            response.headers.set(
                'Content-Type', 'application/json; charset=utf-8')
            response.status_code = 401
            return response
    except:
        # Message to send in case of error.
        response = jsonify(
            {"msg": "Error when creating a tocken.", "tocken": None})
        response.headers.set('Content-Type', 'application/json; charset=utf-8')
        response.status_code = 401
        return response
