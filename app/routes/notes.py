from flask import Blueprint, jsonify, request
from util.tokens import validate_tocken
from config.env import USER_GITHUB, REPO_NOTES
from config.vars import EXTENSIONS_IMAGES
from util.validations import validate_extension
import requests
import tempfile

notes_page = Blueprint("notes__page", __name__)

api_github_notes = f"https://api.github.com/repos/{USER_GITHUB}/{REPO_NOTES}/contents"


@notes_page.before_request
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


@notes_page.route("/subject-matter", methods=["GET"])
def getSubjectMatterByRepo():
    """
    Devuelve una lista de asignaturas y sus URLs obtenidas de una API de GitHub.

    Returns:
        JSON: Un objeto JSON que contiene un mensaje de éxito, la cantidad de asignaturas encontradas, 
        la lista de asignaturas y la lista de URLs.
    Raises:
        Exception: Si la nota no se encuentra en la API de GitHub.
    """
    try:
        # Has la peticion a la api de github
        github__response = requests.get(api_github_notes)
        # Si la peticion devuelve un codigo 404 lanza un código de error
        if github__response.status_code == 404:
            raise Exception("Note not found")
        # Convierte el resultado de a peticion a json
        parse__response = github__response.json()
        # Inicializa dos listas vacias, estas contendran los datos de la api
        # La variable matters guardara el nombre de las materias o carpetas encontradas
        # La variable urls guardara las direcciones a esas carpetas en el repositorio
        matters = []
        urls = []

        # Recorre lo obtenido en la api de github
        for item in parse__response:
            # Si el item es una carpeta entonces guarda sus valores como nombre y su direccion
            if item["type"] == "dir":
                matters.append(item["name"])  # Nombre de la carpeta
                urls.append(item["_links"]["html"])  # Url en el respositorio

        # Crea la respuesta de la ruta con los datos obtenidos
        response = jsonify({
            "msg": "Sucessfull",
            "body": {
                "number_matters": len(matters),
                "matters": matters,
                "urls": urls
            }
        })
        # Asigna el codigo de respuesta de la ruta en este caso 200
        response.status_code = 200
        # Retorna la respuesta de la api
        return response
    except:
        # Crea la respuesta de error para la ruta
        response = jsonify({
            "msg": "Error al obtener las notas"
        })
        # Asignael codigo de error de la respuesta en este caso 404
        response.status_code = 404
        # Retorna la respuesta de la api
        return response


@notes_page.route("/<string:matter>", methods=["GET"])
def getNotesByMatterByRepo(matter: str):
    """
    Devuelve una lista de notas obtenidas de una API de GitHub que corresponden a la materia especificada.

    Args:
        matter (str): El nombre de la materia a buscar notas.

    Returns:
        JSON: Un objeto JSON que contiene un mensaje de éxito, el nombre de la materia y una lista de notas que 
        pertenecen a esa materia. Cada nota tiene un nombre, la URL a la página en el repositorio que contiene 
        la nota y la URL al contenido de la nota.

    Raises:
        Exception: Si la nota no se encuentra en la API de GitHub.
    """
    try:
        # Hace una petición a la API de GitHub para obtener las notas de la materia
        github__response = requests.get(f"{api_github_notes}/{matter}")

        # Si la petición devuelve un código 404, lanza un error
        if github__response.status_code == 404:
            raise Exception("Note not found")

        # Convierte la respuesta a un objeto JSON
        github__response = github__response.json()

        # Inicializa una lista vacía para almacenar las notas
        notes = []

        # Recorre los elementos obtenidos en la respuesta de la API de GitHub
        for item in github__response:
            # Si el elemento es un archivo, se agrega a la lista de notas
            if item["type"] == "file":
                # Extrae el nombre de la nota
                name = item["name"]
                # Extrae el link del archivo en el repositorio
                repo_url = item["_links"]["html"]
                # Extrae el link del contenido del archivo
                download_url = item["download_url"]
                # Agrega los datos a la lista
                notes.append({
                    "name": name,  # Nombre del archivo de nota
                    # URL al archivo en el repositorio
                    "url": repo_url,
                    # URL al contenido del archivo de nota
                    "url_content": download_url,
                    # URL de la api que contiene el contenido del documento
                    "api_url_content": f"{request.host_url}api/notes/note/{matter}/{name}"
                })

        # Crea la respuesta de la ruta con los datos obtenidos
        response = jsonify({
            "msg": "Susscefull",
            "body": {
                "matter": matter,
                "notes": notes
            }
        })
        # Asigna el código de respuesta de la ruta en este caso 200
        response.status_code = 200
        # Retorna la respuesta de la API
        return response

    except:
        # Crea la respuesta de error para la ruta
        response = jsonify({
            "msg": "Failed to find notes"
        })
        # Asigna el código de error de la respuesta en este caso 404
        response.status_code = 404
        # Retorna la respuesta de la API
        return response


@notes_page.route("/all", methods=["GET"])
def getAllNotesByRepo():
    """
    Obtiene todas las notas de un repositorio de GitHub. Devuelve una lista de objetos JSON que contienen el nombre de la nota,
    la asignatura a la que pertenece y la URL del contenido.

    Returns:
        JSON: Un objeto JSON que contiene un mensaje de éxito, la cantidad de notas encontradas, y una lista de objetos JSON que 
        contienen el nombre de la nota, la asignatura a la que pertenece y la URL del contenido.
    Raises:
        Exception: Si la nota no se encuentra en la API de GitHub.
    """
    try:
        # Hace la petición a la API de GitHub
        github__response = requests.get(f"{api_github_notes}")
        # Si la petición devuelve un código 404, lanza un error
        if github__response.status_code == 404:
            raise Exception("Note not found")
        # Convierte el resultado de la petición a JSON
        github__response = github__response.json()
        notes = []

        # Recorre los objetos obtenidos de la petición
        for item in github__response:
            # Si el objeto es una carpeta, se almacena el nombre de la carpeta en la variable matter
            if item["type"] == "dir":
                matter = item["name"]
                # Se hace una petición a la API de GitHub para obtener los objetos contenidos en la carpeta
                github__response__by__theme = requests.get(
                    f"{api_github_notes}/{matter}")
                github__response__by__theme = github__response__by__theme.json()

                # Se recorren los objetos obtenidos de la petición por carpeta
                for item_matter in github__response__by__theme:
                    # Extrae el nombre de la nota
                    name = item["name"]
                    # Extrae el link del archivo en el repositorio
                    repo_url = item["_links"]["html"]
                    # Extrae el link del contenido del archivo
                    download_url = item["download_url"]
                    # Agrega los datos a la lista
                    # Si el objeto es un archivo, se agrega a la lista notes
                    if item_matter["type"] == "file":
                        notes.append({
                            "name": name,
                            "url": repo_url,
                            "url_content": download_url,
                            "api_url_content": f"{request.host_url}api/notes/note/{matter}/{name}",
                            "matter": matter
                        })

        # Se crea la respuesta de la ruta con los datos obtenidos
        response = jsonify({
            "msg": "Sucessfull",
            "body": {
                "number_notes": len(notes),
                "notes": notes
            }
        })
        # Se asigna el código de respuesta de la ruta, en este caso 200
        response.status_code = 200
        # Se retorna la respuesta de la API
        return response
    except:
        # Se crea la respuesta de error para la ruta
        response = jsonify({
            "msg": "Failed to find notes"
        })
        # Se asigna el código de error de la respuesta, en este caso 404
        response.status_code = 404
        # Se retorna la respuesta de la API
        return response


@notes_page.route("/note/<string:matter>/<string:filename>", methods=["GET"])
def getDataByRoute(matter: str, filename: str):
    """
    Devuelve el contenido de un archivo de notas específico, dada la materia y el nombre de archivo proporcionados.

    Args:
        matter (str): El nombre de la materia en la que se encuentra el archivo de notas.
        filename (str): El nombre del archivo de notas que se desea recuperar.

    Returns:
        JSON: Un objeto JSON que contiene un mensaje de éxito, el nombre de la materia, el nombre del archivo de notas y su contenido.

    Raises:
        Exception: Si el archivo de notas no se encuentra en la materia especificada.
    """
    try:
        # Hace una petición GET a la API de GitHub utilizando el nombre de la materia proporcionado.
        github__response = requests.get(f"{api_github_notes}/{matter}")
        # Si la petición devuelve un código 404, lanza una excepción.
        if github__response.status_code == 404:
            raise Exception("Note not found")
        # Convierte el resultado de la petición a formato JSON.
        github__response = github__response.json()
        # Inicializa una variable de cadena vacía que contendrá el contenido del archivo de notas.
        content = ""

        # Recorre los elementos obtenidos de la materia especificada en la API de GitHub.
        for item in github__response:
            # Si el elemento es un archivo y su nombre coincide con el nombre del archivo proporcionado,
            # guarda su URL de descarga y descarga su contenido.
            if item["type"] == "file" and item["name"] == filename:
                print(item["download_url"])
                content = requests.get(item["download_url"])
                content = content.text

        # Crea la respuesta de la ruta con los datos obtenidos.
        response = jsonify({
            "msg": "Successful",
            "body": {
                "matter": matter,
                "note": filename,
                "content": content
            }
        })
        # Asigna el código de respuesta de la ruta en este caso 200.
        response.status_code = 200
        # Retorna la respuesta de la API.
        return response

    except:
        # Crea la respuesta de error para la ruta.
        response = jsonify({
            "msg": "Failed to find notes"
        })
        # Asigna el código de error de la respuesta en este caso 404.
        response.status_code = 404
        # Retorna la respuesta de la API.
        return response


@notes_page.route("/assets/<string:matter>", methods=["GET"])
def getImagesAndAssets(matter: str):
    """
    Obtiene imágenes y activos de una asignatura a partir de la API de GitHub.

    Args:
        matter (str): La materia de la que se quieren obtener las imágenes y activos.

    Returns:
        JSON: Un objeto JSON que contiene un mensaje de éxito y la lista de imágenes y activos encontrados
        en la materia.

    Raises:
        Exception: Si la materia o los activos no se encuentran en la API de GitHub.
    """
    try:
        # Hace una petición a la API de GitHub para obtener la materia en cuestión
        github_response = requests.get(f"{api_github_notes}/{matter}")
        # Si la petición devuelve un código 404, lanza un código de error
        if github_response.status_code == 404:
            raise Exception("Note not found")
        # Convierte la respuesta de la petición en formato JSON
        github_response = github_response.json()
        # Inicializa una lista vacía que contendrá las imágenes y activos encontrados en la materia
        images = []

        # Recorre la respuesta de la API de GitHub
        for item in github_response:
            # Si el item es una carpeta, busca dentro de ella los activos
            if item["type"] == "dir":
                # Hace una petición a la API de GitHub para obtener los activos de la carpeta
                github_folder_assets = requests.get(item["url"])
                # Si la petición devuelve un código 404, lanza un código de error
                if github_folder_assets.status_code == 404:
                    raise Exception("Note not found")
                # Convierte la respuesta de la petición en formato JSON
                github_folder_assets = github_folder_assets.json()
                # Inicializa una lista vacía que contendrá las imágenes encontradas en la carpeta
                images_folder = []
                folder = item["name"] # Obtener el folder donde se encuentran las imagenes

                # Recorre la respuesta de la API de GitHub
                for item_folder in github_folder_assets:
                    # Valida que el archivo tenga la extensión correspondiente (png, jpeg, o jpg)
                    validation = validate_extension(
                        EXTENSIONS_IMAGES, item_folder["name"])

                    # Si el archivo tiene la extensión correspondiente, agrega su información a la lista de imágenes
                    if validation:
                        name = item_folder["name"]
                        download_url = item_folder["download_url"]
                        images_folder.append({
                            "name": name,
                            "url": download_url,
                            "api_url_content": f"{request.host_url}api/assets/note/{matter}/{folder}/{name}"
                        })

                # Agrega la información de las imágenes encontradas en la carpeta a la lista de imágenes
                images.append({
                    "images": images_folder,
                    "folder": folder
                })

        # Si no se encontraron imágenes, devuelve un mensaje de error
        if len(images) == 0:
            response = jsonify({
                "msg": "No image was found"
            })
            response.status_code = 404
        # Si se encontraron imágenes, devuelve la información de las imágenes en un objeto JSON
        else:
            response = jsonify({
                "msg": "Susscefull",
                "body": {
                    "matter": matter,
                    "images": images
                }
            })
            response.status_code = 200
        # Retorna la respuesta de la API
        return response
    except:
        # Si no se pudo encontrar la materia o los activ
        response = jsonify({
            "msg": "Failed to find notes"
        })
        response.status_code = 404
        return response
