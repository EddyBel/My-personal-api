from flask import Blueprint, jsonify, request
from util.tokens import validate_tocken
from util.formatters import parse_yaml_frontmatter, format_as_markdown_frontmatter
from config.env import USER_GITHUB, REPO_NOTES, TOKEN_GITHUB
from config.vars import EXTENSIONS_IMAGES
from util.validations import validate_extension
from app.services.github import GITHUB

notes_page = Blueprint("notes__page", __name__)

github = GITHUB(USER_GITHUB, TOKEN_GITHUB)


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
        response = github.get_repository_folders(REPO_NOTES)
        # Inicializa dos listas vacias, estas contendran los datos de la api
        # La variable matters guardara el nombre de las materias o carpetas encontradas
        # La variable urls guardara las direcciones a esas carpetas en el repositorio
        matters = []
        urls = []

        # Recorre lo obtenido en la api de github
        for item in response:
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
        response = github.get_files_in_repository_folder(REPO_NOTES, matter)

        # Inicializa una lista vacía para almacenar las notas
        notes = []

        # Recorre los elementos obtenidos en la respuesta de la API de GitHub
        for item in response:
            # Si el elemento es un archivo, se agrega a la lista de notas
            if item["type"] == "file":
                # Extrae el nombre de la nota
                name = item["name"]
                # Extrae el link del archivo en el repositorio
                repo_url = item["_links"]["html"]
                # Extrae el link del contenido del archivo
                download_url = item["download_url"]
                # Obten el contenido de l nota
                raw_content = github.get_data(download_url, type="text")
                # Extrae la metadata del contenido
                metadata = parse_yaml_frontmatter(raw_content)
                # Agrega los datos a la lista
                notes.append({
                    "name": name,
                    "url": repo_url,
                    "url_content": download_url,
                    "url_api": f"{request.host_url}api/notes/content/{matter}/{name}",
                    "metadata": metadata
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
        # Hace la petición a la API de GitHub para obtener las carpetas en el repositorio
        response_folders = github.get_repository_folders(REPO_NOTES)
        # Variable que almacenara las notas del repositorio
        notes = []

        # Recorre los objetos obtenidos de la petición
        for item_folder in response_folders:
            # Se almacena el nombre de la carpeta en la variable matter
            matter = item_folder["name"]
            # Se hace una petición a la API de GitHub para obtener los objetos contenidos en la carpeta
            response_files = github.get_files_in_repository_folder(
                REPO_NOTES, matter)

            # Se recorren los objetos obtenidos de la petición por carpeta
            for item_matter in response_files:
                # Extrae el nombre de la nota
                name = item_matter["name"]
                # Extrae el link del archivo en el repositorio
                repo_url = item_matter["_links"]["html"]
                # Extrae el link del contenido del archivo
                download_url = item_matter["download_url"]
                # Obten el contenido de l nota
                raw_content = github.get_data(download_url, type="text")
                # Extrae la metadata del contenido
                metadata = parse_yaml_frontmatter(raw_content)
                # Agrega los datos a la lista
                # Si el objeto es un archivo, se agrega a la lista notes
                if item_matter["type"] == "file":
                    notes.append({
                        "name": name,
                        "url": repo_url,
                        "url_content": download_url,
                        "url_api": f"{request.host_url}api/notes/content/{matter}/{name}",
                        "matter": matter,
                        "metadata": metadata
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


@notes_page.route("/content/<string:matter>/<string:filename>", methods=["GET"])
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
        response = github.get_files_in_repository_folder(REPO_NOTES, matter)
        # Inicializa una variable de cadena vacía que contendrá el contenido del archivo de notas.
        raw_content = ""
        content = ""
        metadata = ""

        # Recorre los elementos obtenidos de la materia especificada en la API de GitHub.
        for item in response:
            # Si el elemento es un archivo y su nombre coincide con el nombre del archivo proporcionado,
            # guarda su URL de descarga y descarga su contenido.
            if item["name"] == filename:
                raw_content = github.get_data(
                    item["download_url"], type="text")
                metadata = parse_yaml_frontmatter(content)
                content = format_as_markdown_frontmatter(raw_content)

        # Crea la respuesta de la ruta con los datos obtenidos.
        response = jsonify({
            "msg": "Successful",
            "body": {
                "matter": matter,
                "note": filename,
                "metadata": metadata,
                "content": content,
                "raw_content": raw_content,
            }
        })
        # Asigna el código de respuesta de la ruta en este caso 200.
        response.status_code = 200
        # Retorna la respuesta de la API.
        return response

    except Exception as e:
        print("Ocurrió un error:", e)
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
        response_folder = github.get_subfolders_in_repository_folder(
            REPO_NOTES, matter)
        # Inicializa una lista vacía que contendrá las imágenes y activos encontrados en la materia
        images = []

        # Recorre la respuesta de la API de GitHub
        for item_folder in response_folder:
            # Hace una petición a la API de GitHub para obtener los archivos de la carpeta
            response_files = github.get_data(item_folder["url"], "json")
            # Inicializa una lista vacía que contendrá las imágenes encontradas en la carpeta
            images_folder = []
            # Obtener el folder donde se encuentran las imagenes
            folder = item_folder["name"]

            # Recorre la respuesta de la API de GitHub
            for item_file in response_files:
                # Valida que el archivo tenga la extensión correspondiente (png, jpeg, o jpg)
                validation = validate_extension(
                    EXTENSIONS_IMAGES, item_file["name"])
                # Si el archivo tiene la extensión correspondiente, agrega su información a la lista de imágenes
                if validation:
                    name = item_file["name"]
                    download_url = item_file["download_url"]
                    images_folder.append({
                        "name": name,
                        "url": download_url,
                        "url_api": f"{request.host_url}api/assets/note/{matter}/{folder}/{name}"
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
