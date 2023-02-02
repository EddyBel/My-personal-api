from flask import Blueprint, jsonify, request
from util.files import read_file_json, read_file_markdown
from util.date import get_date_of_birth
from util.formatters import read_markdown_string
from util.tokens import validate_tocken
from config.paths import PATH_USER_DATA, PATH_USER_BIOGRAFHY, PATH_USER_SKILLS, PATH_USER_PROYECTS

about_pages = Blueprint("about_pages", __name__)


@about_pages.before_request
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
        return response, 401


@about_pages.route("/info", methods=['GET'])
def getAboutInfo():
    """This address is used to serve the personal or basic data obtained from the json file "user.json".

    Returns:
        (Response): Returns the requested content and a message.
    """

    try:
        # Get the content of the json file
        content = read_file_json(PATH_USER_DATA)

        # Calculate age according to date of birth.
        try:
            # Obtain the date of birth of the document
            date_of_birth = content["date of birth"]
            # Calculate current age
            age = get_date_of_birth(date_of_birth)
            # Add the data to the data dictionary
            content["age"] = age
            content["age string"] = f"{age} años"
        except:
            pass

        # Content of the api
        response = jsonify({"msg": "Successful", "body": content})
        response.headers.set('Content-Type', 'application/json; charset=utf-8')
        response.status_code = 200
        return response
    except:
        # Content of the api
        response = jsonify(
            {"msg": "Error getting the requested content.", "body": None})
        response.headers.set('Content-Type', 'application/json; charset=utf-8')
        response.status_code = 401
        return response


@about_pages.route('/biography', methods=['GET'])
def getAboutDescription():
    """This address is used to serve the biography data obtained from the markdown file "about_me.md".

    Returns:
        (Response): Returns the requested content and a message.
    """

    try:
        # Get the contents of the markdown file
        content = read_file_markdown(PATH_USER_BIOGRAFHY)
        # Format the content as an array with the specified features
        content = read_markdown_string(content)

        # Content of the api
        response = jsonify({"msg": "Successful", "body": content})
        response.headers.set('Content-Type', 'application/json; charset=utf-8')
        response.status_code = 200
        return response
    except:
        # Content of the api
        response = jsonify(
            {"msg": "Error getting the requested content.", "body": None})
        response.headers.set('Content-Type', 'application/json; charset=utf-8')
        response.status_code = 401
        return response


@about_pages.route('/skills', methods=['GET'])
def getAboutSkills():
    """This address is used to serve the skills data obtained from the json file "skills.json".

    Returns:
        (Response): Returns the requested content and a message.
    """

    try:
       # Get the content of the json file
        content = read_file_json(PATH_USER_SKILLS)
        # Obtain the number of languages learned
        languages = content["skills"]["languages"]
        count_languages = len(languages)

        # Obtain the number of frameworks learned
        frameworks = content["skills"]["frameworks_and_tools"]
        count_frameworks = len(frameworks)

        # Obtain the number of other skills learned
        other_skills = content["skills"]["other_skills"]
        count_other_skills = len(other_skills)

        # Add data to the array
        content["count_languages"] = count_languages
        content["count_frameworks"] = count_frameworks
        content["count_other_skills"] = count_other_skills

        # Content of the api
        response = jsonify({"msg": "Successful", "body": content})
        response.headers.set('Content-Type', 'application/json; charset=utf-8')
        response.status_code = 200
        return response
    except:
        # Content of the api
        response = jsonify(
            {"msg": "Error getting the requested content.", "body": None})
        response.headers.set('Content-Type', 'application/json; charset=utf-8')
        response.status_code = 401
        return response


@about_pages.route('/proyects', methods=['GET'])
def getAboutProyects():
    """This address is used to serve project data obtained from the json file "projects.json".

    Returns:
        (Response): Returns the requested content and a message.
    """

    try:
        # Get file contents
        content = read_file_json(PATH_USER_PROYECTS)

        # Browse through the projects and assign them the path to their respective images.
        for proyect in content:
           # Create the path to the project images
            name_image = proyect["background"]
            host = request.host_url
            base_path = f"{host}api/assets/img/{name_image}"
            proyect["background"] = base_path

        # Content of the api
        response = jsonify({"msg": "Successful", "body": content})
        response.headers.set('Content-Type', 'application/json; charset=utf-8')
        response.status_code = 200
        return response

    except:
        # Content of the api
        response = jsonify(
            {"msg": "Error getting the requested content.", "body": None})
        response.headers.set('Content-Type', 'application/json; charset=utf-8')
        response.status_code = 401
        return response
