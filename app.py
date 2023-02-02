from flask import Flask, render_template, redirect
from flask_cors import CORS
from app.routes.about import about_pages
from app.routes.static import files_statics
from app.routes.auth import auth_pages
from app.routes.index import index_page
from app.routes.message import message_pages
from config.vars import WHITE_LIST
from config.env import HOST, PORT, DEVELOPMENT

# ----------------------------------------- Config APP

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app, origins=WHITE_LIST)

# ----------------------------------------- Registration of available pages

app.register_blueprint(index_page, url_prefix="/api")
app.register_blueprint(about_pages, url_prefix="/api/personal")
app.register_blueprint(files_statics, url_prefix="/api/assets")
app.register_blueprint(auth_pages, url_prefix="/api/auth")
app.register_blueprint(message_pages, url_prefix="/api/message")


# ------------------------------------------ Redirect pages

@app.route('/', methods=['GET'])
def initAPI():
    return redirect("/api")

# ------------------------------------------- Page to be rendered if nothing else is found.


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(405)
def page_not_found(e):
    return render_template("405.html"), 405


if __name__ == "__main__":
    # Runs the server
    app.run(port=int(PORT), debug=bool(DEVELOPMENT), host=HOST)
