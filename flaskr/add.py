from flask import Blueprint, render_template, request
from .db import get_db

bp = Blueprint("add", __name__, url_prefix="/add")


@bp.route("/", methods=("GET", "POST"))
def add():
    if request.method == "GET":
        return render_template("add.html")

    json = request.get_json()
    word = json.get("word").strip().lower()
    comments = json.get("comments").strip()

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT EXISTS(SELECT 1 FROM words WHERE word = %s)", (word,))
        exists = cursor.fetchone()[0]
        if exists:
            return "Word already exists", 400

        cursor.execute(
            """
            INSERT INTO words (word, comment, interval_days)
            VALUES (%s, %s, %s)
            """,
            (word, comments, 1),  # interval_days starts at 1
        )
        db.commit()
    except:
        return "Failed to add the word.", 400

    return "Success"
