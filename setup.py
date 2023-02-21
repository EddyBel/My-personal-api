from setuptools import setup

setup(
    name="My_personal_api",  # Nombre del proyecto
    version="2.0.0",  # Versión del proyecto
    # Descripción breve del proyecto
    description="The project is an API that provides information about you and allows users to access your blog posts and notes in markup format.",
    # Descripción larga del proyecto
    long_description="The project is an API developed using Flask, a Python web development framework. The API provides information about you and allows users to access your blog posts and notes in markdown format. It also has additional functionality for sending messages and retrieving images and documents. This API is a complete solution for sharing your content in an easy and accessible way.",
    author="Eduardo Antonio Rangel Serrano",  # Nombre del autor del proyecto
    # Correo electrónico del autor del proyecto
    author_email="kratos61918@gmail.com",
    url="",  # URL del sitio web del proyecto
    packages=[""],  # Paquetes incluidos en el proyecto
    classifiers=[  # Clasificadores para el proyecto, por ejemplo, para qué versión de Python es compatible
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Versión mínima de Python necesaria para el proyecto
    install_requires=[  # Dependencias necesarias para el proyecto
        "autopep8 == 2.0.1",
        "bcrypt == 4.0.1",
        "cachetools == 5.3.0",
        "certifi == 2022.12.7",
        "charset-normalizer == 3.0.1",
        "click == 8.1.3",
        "colorama == 0.4.6",
        "cssselect == 1.2.0",
        "cssutils == 2.6.0",
        "dnspython == 2.3.0",
        "Flask == 2.2.2",
        "Flask-Cors == 3.0.10",
        "idna == 3.4",
        "itsdangerous == 2.1.2",
        "Jinja2 == 3.1.2",
        "lxml == 4.9.2",
        "MarkupSafe == 2.1.1",
        "premailer == 3.10.0",
        "pycodestyle == 2.10.0",
        "PyJWT == 2.6.0",
        "pymongo == 4.3.3",
        "python-dotenv == 0.21.1",
        "PyYAML == 6.0",
        "requests == 2.28.2",
        "six == 1.16.0",
        "urllib3 == 1.26.14",
        "Werkzeug == 2.2.2",
        "yagmail == 0.15.293"
    ],
)
