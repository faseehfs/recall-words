import os

from flask import Flask, Blueprint, render_template, request, url_for
from .db import get_db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        MYSQL_HOST="localhost",
        MYSQL_USER="recall_words_user",
        MYSQL_PASSWORD="recall_words_password",
        MYSQL_DATABASE="recall_words_db",
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db

    db.init_app(app)

    # ---

    @app.route("/")
    def home():
        return f"<a href='{url_for('add')}'>Add</a>"

    @app.route("/add/", methods=("GET", "POST"))
    def add():
        """
        GET: Returns the add page.
        POST: Accepts a FormData containing "word" and "comments" as the body.
        """
        if request.method == "GET":
            return render_template("add.html")

        word = request.form.get("word").strip().lower()
        if word is None:
            return "Word is empty.", 400

        comments = request.form.get("comments", "").strip()

        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                "SELECT EXISTS(SELECT 1 FROM words WHERE word = %s)", (word,)
            )
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

        return "Word added."

    return app
