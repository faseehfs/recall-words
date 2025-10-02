from flask import Blueprint

bp = Blueprint("add", __name__, url_prefix="/add")


@bp.route("/", methods=("GET", "POST"))
def add():
    return "This is the adding page."
