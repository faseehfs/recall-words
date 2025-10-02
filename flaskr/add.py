from flask import Blueprint, render_template

bp = Blueprint("add", __name__, url_prefix="/add")


@bp.route("/", methods=("GET", "POST"))
def add():
    return render_template("add.html")
