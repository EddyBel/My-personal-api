from flask import Blueprint, request, jsonify
from config.env import SECRET_EMAIL_SENDER, SECRET_PASSWORD_SENDER, SECRET_EMAILS_ADDRESSEE
from config.vars import NAME_BASE_API
from util.tokens import validate_tocken
import yagmail

message_pages = Blueprint('message_pages', __name__)


@message_pages.before_request
def verifyTockenForAboutInfo():
    """This function verifies that the client or user has passed an access token through the headers with the X-Tocken property, if this property does not exist or is not valid, access to the information will not be given.

    Returns:
        (Response | None): Returns a response in json format if an error occurs, if everything is correct let the next function enter the one that has the data.
    """

    # Verify that the token is found and valid.
    try:
        # Obtain the tocken with the tag "X-Tocken" and verify it with the function created to validate tockens.
        tocken_header = request.headers['X-Tocken']
        return validate_tocken(tocken=tocken_header, output=False)
    except:
        # This error is usually obtained when there is no X-Tocken tag, it responds with json with the requested message.
        response = jsonify({
            "msg": "The header does not contain any 'X-Tocken' property, please create a tocken before requesting information.",
            "msg web": "Hi, this api is in charge of serving some data and other materials for my web pages and projects like my portfolio, it hosts several types of methods like sending messages etc. In order to use this api is required the user and password this to generate a tocken that gives the authorization to the api.",
            "body": None
        })
        response.status_code = 401
        response.headers.set('Content-Type', 'application/json; charset=utf-8')
        return response


@message_pages.route('/gmail', methods=['POST'])
def sendToMessageInGmail():
    """This address allows you to send an email from gmail.

    Returns:
        (Response): It sends a message in json format that indicates the status of the function if it is concrete or if there was an error.
    """

    try:
        # Extracts the content passed by the request.
        content = request.get_json()
        url_origin = content["url"]
        subject = content["subject"]
        user_name = content["propertys"]["name"]
        user_last_name = content["propertys"]["last_name"]
        user_email = content["propertys"]["email"]
        user_phone = content["propertys"]["phone"]
        message = content["message"]
        # Special texts created as lists.
        greetings = f"<h1>Hola {NAME_BASE_API}</h1>"
        direccion_origin = f"<h4>Origen '{url_origin}'</h4>"
        item_name = f"<li>Soy {user_name} {user_last_name}</li>"
        item_email = f"<li>Mi correo es {user_email}</li>"
        item_phone = f"<li>Mi telefono es {user_phone}</li>"
        propertys = f"<ul>{item_name}{item_email}{item_phone}</ul>"
        emails_addressee = SECRET_EMAILS_ADDRESSEE.split(", ")

        try:
            # Create the email connection.
            yag = yagmail.SMTP(user=SECRET_EMAIL_SENDER,
                               password=SECRET_PASSWORD_SENDER)
            # Sends the message with the properties extracted before.
            yag.send(emails_addressee, subject, [
                     greetings, direccion_origin, propertys, message])
            # Message sent when the message is successfully sent.
            response = jsonify(
                {"msg": "Message sent successfully", "body": content})
            response.headers.set(
                'Content-Type', 'application/json; charset=utf-8')
            response.status_code = 200
            return response
        except:
            # Error message in the event of an error in data transmission.
            response = jsonify({"msg": "Error sending message"})
            response.headers.set(
                'Content-Type', 'application/json; charset=utf-8')
            response.status_code = 401
            return response
    except:
        # In case of an error in obtaining the data send error message.
        response = jsonify(
            {"msg": "There was an error in extracting the required data."})
        response.headers.set('Content-Type', 'application/json; charset=utf-8')
        response.status_code = 401
        return response
