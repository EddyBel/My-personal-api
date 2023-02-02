<h1 align="center" >My personal api</h1>

<div style="display:flex;justify-content:center;align-items:center;gap:10px;flex-wrap:wrap;">
    <img align="center" src="https://img.shields.io/github/last-commit/EddyBel/My-personal-api?color=%23AED6F1&style=for-the-badge" />
    <img align="center" src="https://img.shields.io/github/license/EddyBel/My-personal-api?color=%23EAECEE&style=for-the-badge" />
    <img align="center" src="https://img.shields.io/github/languages/top/EddyBel/My-personal-api?color=%23F9E79F&style=for-the-badge" />
    <img align="center" src="https://img.shields.io/github/languages/count/EddyBel/My-personal-api?color=%23ABEBC6&style=for-the-badge" />
    <img align="center" src="https://img.shields.io/github/languages/code-size/EddyBel/My-personal-api?color=%23F1948A&style=for-the-badge" />
</div>

---

The project is an API developed using Flask, a Python web development framework. The API provides information about you and allows users to access your blog posts and notes in markdown format. It also has additional functionality for sending messages and retrieving images and documents. This API is a complete solution for sharing your content in an easy and accessible way.

## Why ? :relieved:

The project was created with the goal of simplifying the way data is provided and accessed in personal web projects, such as a portfolio, blog or any other project that requires access to such information. The API developed in Flask provides a unique and efficient solution for sharing and accessing this data in a simple way, allowing users to focus on other important aspects of their web projects. The combination of an easy-to-use interface and a wealth of functionality makes this API a valuable tool for anyone who needs to share and access their data quickly and efficiently.

## Prerequisites

These are some of the tools or programs needed to run the program.

- Python Version 3.9 and higher
- Docker
- Virtualenv

## <a id="environment_variables" /> Required environment variables

- :wrench: **PORT**: Specifies the port that the API will use to listen for requests.
- :wrench: **DEBUG**:Indicates whether the API is in development or production mode. This can affect how errors and API responses are handled.
- :wrench: **HOST**: Specifies the host that the API will use to listen for requests. It is recommended to use 0.0.0.0.0 for Docker packaging.
- :wrench: **SECRET_KEY**: A text string used to encrypt and create access tokens.
- :wrench: **ROOT_USERNAME**: The user name with API access permissions.
- :wrench: **ROOT_PASSWORD**:The password associated with the user name with API access permissions.
- :wrench: **EMAIL_SENDER**: The email that will be used to send emails through Gmail.
- :wrench: **PASSWORD_SENDER**: The password generated for the application to be able to send e-mails through Gmail.
- :wrench: **EMAILS_ADDRESSEE**: A list of emails to which the emails will be sent. These emails are separated by the string ", ".

## Configurations

At the moment the data to be served is in the **data** folder, there is a data structure in Json and markdown format that can be replaced by the data you need.

In addition, the **config** folder contains several api configuration files.

- **paths.py** - This file contains the addresses to the internal files that need to be read, such as data files.
- **env.py** - This file stores all environment variables and stores them in variables for use throughout the project.
- **vars.py** - This file stores global settings for general use throughout the project.

## Project execution

In order to run this project it is recommended to use a docker container, but it can also be run in a python virtual environment.

The first thing to do is to clone the repository on your local machine and move into the project.

```bash
git clone https://github.com/EddyBel/My-personal-api.git
```

```bash
cd My-personal-api
```

### Docker

To run this project with docker it is only necessary to have docker installed. The dockerfile contains instructions on how the app should be packaged.

This container uses the :link:[python:3.9.16-alpine3.17](https://hub.docker.com/layers/library/python/3.9.16-alpine3.17/images/sha256-030102bf02171eb24efc32cb7a630d369ddf10f2c562733bb95b9b8edc6bf7f8?context=explore) image which allows it to be lighter and faster to package.

The first step is to package the app with the docker _build_ command as follows.

```bash
docker build -t container-name .
```

To run the container it is necessary to add environment variables as needed.

```bash
docker run \
    -e PORT=3000 \
    -e DEBUG=False \
    -e SECRET_KEY=secret_string \
    -e ROOT_USERNAME=username \
    -e ROOT_PASSWORD=1234 \
    -e EMAIL_SENDER=example@gmail.com \
    -e PASSWORD_SENDER=123456 \
    -e EMAILS_ADDRESSEE=example@gmail.com, example2@gmail.com \
    --name server \
    -p 5050:3000 \
    container-name
```

```bash
 docker run -e PORT=3000 -e DEBUG=False -e SECRET_KEY=secret_string -e ROOT_USERNAME=username -e ROOT_PASSWORD=1234 -e
 EMAIL_SENDER=example@gmail.com -e PASSWORD_SENDER=123456 -e EMAILS_ADDRESSEE="example@gmail.com, example2@gmail.com" --name server -p 5050:3000 container-name
```

This command will run the container on the internal port 3000 but on the external port 5050 these values can be modified at will, at the end the project will run on localhost:5050.

### Virtualenv

Inside the project folder it is necessary to create a python virtual environment to run the project, this will be done with the free python [Virualenv](https://virtualenv.pypa.io/en/latest/) with the following command.

```bash
python.exe -m venv env
```

In this case a virtual environment with the name **env** is being created, this will be the working environment.

The next step is to enter the virtual environment, depending on the platform you are in, this is done in the following way.

> ## Windows
>
> ```bash
> ./env/Scripts/activate
> ```

---

> ## Linux
>
> ```bash
> source ./env/bin/activate
> ```

Once inside the virtual environment all the dependencies for the project must be installed, this will be done with the file "requeriments.txt" located in the root.

```bash
pip install -r requeriments.txt
```

Once all the dependencies are installed, it is important to create an **.env** file in the root of the project, this file must contain the [environment variables](#environment_variables) previously mentioned in the document.

To finish we must run the project, we will do this by executing the **app.py** file.

```bash
python ./app.py
```

The project will run on **localhost** and on the port you have designated in the **.env** file.

## Technologies and tools used

- Python
- Flask
- Docker
- Virtualenv
