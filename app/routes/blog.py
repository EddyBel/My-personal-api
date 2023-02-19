from flask import Blueprint, jsonify, send_file, request, redirect, url_for
from util.validations import validate_strings, validate_extension
from config.env import MONGO, SECRET_ROOT_USERNAME, SECRET_ROOT_PASSWORD
from config.vars import EXTENSIONS_POSTS, EXTENSIONS_IMAGES
from pymongo import MongoClient
from datetime import datetime
from json import loads
from bson import Binary
from functools import wraps

blog_page = Blueprint('blog_page', __name__)

#! TODO TERMINA LAS FUNCIONES PARA OBTENER LOS BLOGS
# * TODO TERMINA LAS FUNCIONES PARA INSERTAR POST A MYSQL, SQL Y FIREBASE


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verificar si el usuario está autenticado
        return redirect(url_for('login'))
        # return f(*args, **kwargs)
    return decorated_function


@blog_page.route('/insert', methods=['GET'])
def insertPostByForm():
    """Send your files from the post route of the get method, through an HTML template

    Returns:
        (Response): Response HTML template.
    """
    return send_file("templates/insert_post.html")


@blog_page.route('/insert', methods=['POST'])
def insertPostInDataBase():
    """Post route that will receive the post files to save them to a database.

    Returns:
        (Response): Program status message if the post was added or not.
    """

    try:
        type = request.form["type"]
        if type == "file":
            post = request.files["post"]
            images = request.files.getlist("assets")
            validation_post = validate_extension(
                EXTENSIONS_POSTS, post.filename)
            images_binarys = []

            if validation_post:
                content = post.read().decode("UTF-8")

                for image in images:
                    validation_img = validate_extension(
                        EXTENSIONS_IMAGES, image.filename)

                    if validation_img:
                        img_binary = Binary(image.read())
                        images_binarys.append({
                            "name": image.filename,
                            "img": img_binary
                        })

        # ---------------------------------------- Conection
        # Mongo
        try:
            client = MongoClient(MONGO)
            db = client["blog"]
            collection = db["post"]
            collection.insert_one({
                "type": "file",
                "content": content,
                "images": images_binarys
            })
            response = jsonify({
                "msg": "The message was sent correctly to mongodb",
                "name": post.filename,
                "content": content
            })
            return response
        # Local
        except:
            pass

    except:
        response = jsonify({
            "msg": "Could not save any post"
        })
        response.status_code = 401
        return response
