from flask import Blueprint, jsonify, send_from_directory, send_file
from os import path
from config.vars import ROOT_DIR

files_statics = Blueprint('files_statics', __name__)


@files_statics.route("/img/<path:filename>", methods=['GET'])
def getToIMGS(filename: str):
    """This path allows access to images in the project, these images are passed as a parameter of the url.

    Args:
        filename (str): Name of the file to search.

    Returns:
        (Response): It can be the requested image if it is found or an error message in json format if it is not found.
    """

    try:
        # Api response
        response = send_file(f"./static/img/{filename}")
        # response.headers.set(
        # 'Content-Type', 'imagen/jpg')
        response.status_code = 200
        return response
    except:
        # Error message to response api
        response = jsonify({
            "msg": "Image not found",
            "image": f"{filename} image not found",
            "name": filename
        })
        response.headers.set(
            'Content-Type', 'application/json; charset=utf-8')
        response.status_code = 401
        return response


@ files_statics.route("/docs/<path:filename>", methods=['GET'])
def getToDocs(filename: str):
    """This path allows access to the project documents, these documents are passed as a parameter of the url.

    Args:
        filename (str): Document to search.

    Returns:
        (Response): It can be the requested document if found or an error message in json format if not found.
    """

    try:
        # Api response
        response = send_file(f"./static/docs/{filename}")
        response.headers.set(
            'Content-Type', 'application/pdf')
        response.status_code = 200
        return response
    except:
        # Error message to response api
        response = jsonify({
            "msg": "Docs not found",
            "file": f"{filename} document not found",
            "path_file": filename
        })
        response.headers.set(
            'Content-Type', 'application/json; charset=utf-8')
        response.status_code = 401
        return response


@ files_statics.route("/web/<path:filename>", methods=['GET'])
def getToCode(filename: str):
    """This path allows access to images in the project, these images are passed as a parameter of the url.

    Args:
        filename (str): Name of the file to search.

    Returns:
        (Response): It can be the requested image if it is found or an error message in json format if it is not found.
    """

    try:
        # Api response
        response = send_file(f"./static/web/{filename}")
        # response.headers.set(
        #     'Content-Type', 'imagen/jpg')
        response.status_code = 200
        return response
    except:
        # Error message to response api
        response = jsonify({
            "msg": "Code not found",
            "image": f"{filename} image not found",
            "path_file": filename
        })
        response.headers.set(
            'Content-Type', 'application/json; charset=utf-8')
        response.status_code = 401
        return response
