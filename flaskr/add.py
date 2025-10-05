from flask import Blueprint, render_template, request

bp = Blueprint("add", __name__, url_prefix="/add")


@bp.route("/", methods=("GET", "POST"))
def add():
    if request.method == "GET":
        return render_template("add.html")

    print(request.data.decode())
    return ""
