import requests


class GITHUB:

    def __init__(self, username: str, token: str) -> None:
        self.username = username
        self.api = f"https://api.github.com/repos/{self.username}"
        self.token = f"Bearer {token}"

    def get_data(self, url: str, type: str = "json"):
        """
            Realiza una solicitud GET a la URL especificada, y devuelve los datos de la respuesta en el formato
            especificado.

            Args:
                url (str): La URL a la que se realizará la solicitud.
                type (str, optional): El formato en el que se espera que estén los datos de la respuesta. Puede ser "json"
                para datos JSON, "text" para datos de texto plano, o cualquier otro valor para cualquier tipo de dato.

            Returns:
                Union[Dict[str, Any], str, Any]: Los datos de la respuesta, en el formato especificado.
        """
        # Realiza una solicitud GET a la URL especificada, incluyendo la autenticación del token en la solicitud.
        response = requests.get(url, headers={'Authorization': self.token})

        # Si la respuesta indica que el recurso no se encuentra, lanza una excepción.
        if response.status_code == 404:
            raise Exception("Faild to request")

        # Si el tipo de datos esperado es JSON, devuelve la respuesta como un diccionario de Python.
        if type == "json":
            return response.json()
        # Si el tipo de datos esperado es texto plano, devuelve la respuesta como una cadena de texto.
        elif type == "text":
            return response.text
        # Si el tipo de datos esperado es "content", devuelve la respuesta como una cadena de texto.
        elif type == "content":
            return response.content
        # Si el tipo de datos esperado no es "json" o "text", devuelve la respuesta tal cual.
        else:
            return response

    def get_repository_folders(self, repo: str):
        """
            Obtiene una lista de nombres de carpetas en el repositorio especificado.

            Args:
                repo (str): El nombre del repositorio.

            Returns:
                List[Dict[str, Any]]: Una lista de diccionarios, donde cada diccionario
                representa una carpeta y contiene información sobre ella.
        """
        # Realiza una solicitud GET a la API de GitHub para obtener el contenido del repositorio.
        # Incluye la autenticación del token en la solicitud.
        response = requests.get(
            url=f"{self.api}/{repo}/contents", headers={'Authorization': self.token})

        # Si la respuesta indica que el recurso no se encuentra, lanza una excepción.
        if response.status_code == 404:
            raise Exception("Faild to request")
        # Convierte la respuesta JSON en un objeto de Python.
        response = response.json()
        # Crea una lista vacía para almacenar los nombres de las carpetas.
        folders = []

        # Itera a través de cada objeto de la respuesta.
        for item in response:
            # Si el objeto es una carpeta, agrega el objeto a la lista de carpetas.
            if item["type"] == "dir":
                folders.append(item)

        # Devuelve la lista de carpetas.
        return folders

    def get_files_in_repository_folder(self, repo: str, folder: str):
        """
            Obtiene una lista de objetos que representan los archivos en la carpeta especificada del
            repositorio especificado.

            Args:
                repo (str): El nombre del repositorio.
                folder (str): El nombre de la carpeta dentro del repositorio.

            Returns:
                List[Dict[str, Any]]: Una lista de diccionarios, donde cada diccionario
                representa un archivo y contiene información sobre él.
        """
        # Realiza una solicitud GET a la API de GitHub para obtener el contenido de la carpeta en el repositorio.
        # Incluye la autenticación del token en la solicitud.
        response = requests.get(
            url=f"{self.api}/{repo}/contents/{folder}", headers={'Authorization': self.token})

        # Si la respuesta indica que el recurso no se encuentra, lanza una excepción.
        if response.status_code == 404:
            raise Exception("Faild to request")

        # Convierte la respuesta JSON en un objeto de Python.
        response = response.json()

        # Crea una lista vacía para almacenar los nombres de los archivos.
        files = []

        # Itera a través de cada objeto de la respuesta.
        for item in response:
            # Si el objeto es un archivo, agrega el objeto a la lista de archivos.
            if item["type"] == "file":
                files.append(item)

        # Devuelve la lista de archivos.
        return files

    def get_subfolders_in_repository_folder(self, repo: str, folder: str):
        """
        Obtiene una lista de diccionarios que representan subcarpetas en una carpeta de un repositorio de GitHub.

        Args:
            self (object): Una referencia a la instancia de la clase.
            repo (str): El nombre del repositorio de GitHub.
            folder (str): El nombre de la carpeta a explorar.

        Returns:
            List[Dict[str, Any]]: Una lista de diccionarios que contienen información sobre las subcarpetas encontradas.
        """
        # Realiza una solicitud HTTP GET a la API de GitHub para obtener el contenido de la carpeta "folder" en el repositorio "repo"
        # utilizando la biblioteca "requests". También se agrega un encabezado de autorización en la solicitud.
        response = requests.get(
            url=f"{self.api}/{repo}/contents/{folder}", headers={'Authorization': self.token})

        # Si el estado de la respuesta es 404, lanza una excepción.
        if response.status_code == 404:
            raise Exception("Faild to request")

        # Convierte la respuesta de formato JSON a un objeto de Python
        response = response.json()

        # Crea una lista vacía que contendrá los diccionarios de las subcarpetas encontradas.
        files = []

        # Itera sobre los elementos de la respuesta de la solicitud.
        for item in response:

            # Si el tipo del elemento es "dir" (es decir, si es una subcarpeta), se agrega a la lista "files".
            if item["type"] == "dir":
                files.append(item)

        # Devuelve la lista "files" con los diccionarios de las subcarpetas encontradas.
        return files
