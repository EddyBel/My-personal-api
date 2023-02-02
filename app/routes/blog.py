from flask import Blueprint, jsonify


blog_page = Blueprint('blog_page', __name__)


@blog_page.route('/', methods=['GET'])
def getAllBlogs():
    return jsonify({"msg": "Blog page"})
