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
