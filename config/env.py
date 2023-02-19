from dotenv import load_dotenv
from os import getenv

# Shit all environment variables.
load = load_dotenv()

USER_GITHUB = getenv("USER_GITHUB")

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
PORT = getenv("PORT") if getenv("PORT") else 3000
# Development
DEVELOPMENT = getenv("DEBUG") if getenv("DEBUG") else False
# hosting
HOST = getenv("HOST") if getenv("HOST") else "0.0.0.0"

# ------------------------------------- Notes config

REPO_NOTES = getenv("REPO_NOTES")

# ------------------------------------- Database config
MONGO = getenv("MONGO")
