import yaml
import re


def read_markdown_string(text: str) -> list:
    """This function is passed a markdown string, and it will look for the titles "#" and separate them with their respective content.

    Args:
        text (str): Content to be formatted.

    Returns:
        list: New dictionary-like content organization structure.
    """

    lines = text.split("\n")
    response = []
    body = []
    title = ""

    for line in lines:
        if line.startswith("#"):
            if title and body:
                response.append({"section": title, "content": body})
                body = []
            title = line.strip("#").strip()
        elif line.strip():
            body.append(line)
    if title and body:
        response.append({"section": title, "content": body})
    return response


def parse_yaml_frontmatter(text):
    # Encontrar el contenido entre las líneas de guiones
    match = re.search(r'---\n(.+?)\n---\n', text, re.DOTALL)
    if not match:
        return None
    frontmatter = match.group(1)

    # Analizar el contenido YAML
    data = yaml.load(frontmatter, Loader=yaml.SafeLoader)

    return data


def format_as_markdown_frontmatter(texto):
    inicio = texto.find("---")
    fin = texto.find("---", inicio+3) + 3
    while inicio >= 0 and fin >= 0:
        texto = texto[:inicio] + texto[fin:]
        inicio = texto.find("---")
        fin = texto.find("---", inicio+3) + 3
    return texto.strip()
