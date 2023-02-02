import json


def read_file_json(name__file: str) -> str:
    '''
            Function that reads a json file and returns its content as a dictionary.

            Params:
                name__file (str): Name of the file to be used.

            Returns:
                (str): Contents of the json file.
    '''

    # Open the json file and retrieve all the lines of content store them in a variable and return the content
    content: str = ""
    with open(name__file, 'r', encoding='UTF-8') as file:
        content = json.load(file)

    return content


def read_file_markdown(name__file: str) -> str:
    """This function reads a markdown file with a path passed as a parameter, and returns the contents of the file as a string

    Args:
        name__file (str): Path markdown file

    Returns:
        str: File contents
    """

    # Open the markdown file and retrieve all the lines of content store them in a variable and return the content
    content: str = ""
    with open(name__file, 'r', encoding='UTF-8') as file:
        content = file.read()

    return content
