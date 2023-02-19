import os


def validate_strings(array_strings: list, value: str):
    """
    Función que valida si un valor dado se encuentra dentro de una lista de strings dada.

    Args:
        array_strings (list): Lista de strings a validar.
        value (str): Valor a buscar dentro de la lista.

    Returns:
        bool: Retorna True si el valor se encuentra en la lista y False si no se encuentra.
    """
    for string in array_strings:
        if value == string:
            return True
    return False


def validate_extension(array_strings: list, value: str) -> bool:
    """
    Verifica si la extensión de un archivo está en una lista de extensiones permitidas.

    Args:
        array_strings (list): Una lista de cadenas de texto que representan las extensiones permitidas.
        value (str): Una cadena de texto que representa el nombre de un archivo.

    Returns:
        bool: Retorna True si la extensión del archivo está en la lista de extensiones permitidas. Retorna False en caso contrario.

    Raises:
        No se generan excepciones en esta función.

    Esta función toma una lista de cadenas de texto y una cadena de texto que representa el nombre de un archivo,
    extrae su extensión y llama a la función 'validate_strings' para verificar si la extensión del archivo se encuentra
    en la lista de extensiones permitidas. Retorna True si la extensión del archivo está en la lista de extensiones permitidas,
    y retorna False en caso contrario.
    """
    name, extension = os.path.splitext(value)
    return validate_strings(array_strings=array_strings, value=extension)
