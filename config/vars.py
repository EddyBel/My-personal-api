from os import getcwd, path

# -------------------------------------- Configurations or global variables

# Indicates the number of days that a tocken will live.
EXPIRATION_DATE_IN_DAYS = 1
# Indicates the base address where the project is located.
ROOT_DIR = path.dirname(getcwd())
# Base name used by the api.
NAME_BASE_API = "Eduardo"
# List of permitted sites
WHITE_LIST = ["http://localhost:5050", "https://eduardorangel.netlify.app"]


# -------------------------------------- List of routes in the api

# List of personal routes
API_ROUTES_PERSONAL = [
    "personal/info",
    "personal/biography",
    "personal/skills",
    "personal/proyects",
]

# List of autentication routes
API_ROUTES_AUTH = [
    "auth/login"
]

# List if assets routes
API_ROUTES_ASSETS = [
    "assets/img/banner_math_my.png",
    "assets/img/banner_notebook.jpg",
    "assets/img/banner_plane_wars.jpg",
    "assets/img/front_about.png",
    "assets/img/front_main.png",
    "assets/docs/CV Ingles.pdf"
]
