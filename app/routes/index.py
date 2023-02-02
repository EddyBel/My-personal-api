from flask import Blueprint, jsonify, request
from config.vars import API_ROUTES_PERSONAL, API_ROUTES_ASSETS, API_ROUTES_AUTH

index_page = Blueprint('index_page', __name__)


@index_page.route('/', methods=['GET'])
def getIndex():

    try:
        # Variables containing values such as host and path lists.
        host = request.host_url
        paths_personal = []
        paths_assets = []
        paths_auths = []

        # It runs through the lists containing part of the routes to be concatenated with the host to create the    final base route.

        for route_personal in API_ROUTES_PERSONAL:
            paths_personal.append(f"{host}api/{route_personal}")

        for route_assets in API_ROUTES_ASSETS:
            paths_assets.append(f"{host}api/{route_assets}")

        for route_auths in API_ROUTES_AUTH:
            paths_auths.append(f"{host}api/{route_auths}")

        # Api response
        response = jsonify({"msg": "Hi, this api is in charge of serving some data and other materials for my web pages and projects like my portfolio, it hosts several types of methods like sending messages etc. In order to use this api is required the user and password this to generate a tocken that gives the authorization to   the api.", "paths": {
            "personal": paths_personal,
            "assets": paths_assets,
            "auths": paths_auths
        }})
        response.status_code = 200
        response.headers.set('Content-Type', 'application/json; charset=utf-8')
        return response
    except:
        # Error message to be sent in the event of a failure.
        response = jsonify({"msg": "Error server"})
        response.headers.set('Content-Type', 'application/json; charset=utf-8')
        response.status_code = 401
        return response
