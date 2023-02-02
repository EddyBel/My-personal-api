from dotenv import load_dotenv
from os import getenv

# Shit all environment variables.
load = load_dotenv()

# ------------------------------------ Stores environment variables.

SECRET_KEY_ENCODE = getenv("SECRET_KEY")
SECRET_ROOT_USERNAME = getenv("ROOT_USERNAME")
SECRET_ROOT_PASSWORD = getenv("ROOT_PASSWORD")

# ------------------------------------- Email environment variables

SECRET_EMAIL_SENDER = getenv("EMAIL_SENDER")
SECRET_PASSWORD_SENDER = getenv("PASSWORD_SENDER")
SECRET_EMAILS_ADDRESSEE = getenv("EMAILS_ADDRESSEE")

# ------------------------------------- WEB CONFIG

# Web port
PORT = getenv("PORT")
# Development
DEVELOPMENT = getenv("DEBUG") if getenv("DEBUG") else True
# hosting
HOST = getenv("HOST") if getenv("HOST") else "0.0.0.0"
