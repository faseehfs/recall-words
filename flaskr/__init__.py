import os

from flask import Flask


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
    from . import add

    db.init_app(app)
    app.register_blueprint(add.bp)

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    return app
