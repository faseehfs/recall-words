import os

from flask import Flask, Blueprint, render_template, request, url_for, jsonify
from . import db


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
        return render_template("home.html")

    @app.route("/add/", methods=("GET", "POST"))
    def add():
        """
        GET: Returns the add page.
        POST: Accepts a FormData containing "word" and "comments" as the body.
        """
        if request.method == "GET":
            return render_template("add.html")

        word = request.form.get("word", "").strip().lower()
        comment = request.form.get("comments", "").strip()

        if not word:
            return jsonify({"message": "Word is empty."}), 400

        if db.word_exists(word):
            return jsonify({"message": "Word already exists."}), 400

        db.add_word(word, comment)

        return jsonify({"message": f"Added {word}."}), 200

    @app.route("/review/", methods=("GET",))
    def review():
        row = db.get_review_word_row()
        if row is None:
            return render_template("congrats.html")
        interval_days = row[4]
        all_interval_days = (1, interval_days, interval_days * 2, interval_days * 4)
        return (
            render_template(
                "review.html",
                word=row[0],
                comment=row[1],
                all_interval_days=all_interval_days,
            ),
            200,
        )

    @app.route("/update-review-date/", methods=("POST",))
    def update_review_date():
        data = request.get_json()
        word = data.get("word")
        interval_days = int(data.get("interval-days"))
        db.update_review_date(word, interval_days)

        return jsonify({"message": "Review updated successfully"}), 200

    @app.route("/browse/", methods=("GET",))
    def browse():
        words_and_comments = db.get_words_and_comments()
        return render_template("browse.html", words_and_comments=words_and_comments)

    @app.route("/delete/<word>/", methods=("GET", "POST"))
    def delete(word):
        db.delete_word(word)
        return jsonify({"message": f"Deleted {word}."}), 200

    return app
