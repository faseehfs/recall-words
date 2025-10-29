import mysql.connector
import click
from flask import g, current_app


def get_db():
    if "db" not in g:
        g.db = mysql.connector.connect(
            host=current_app.config["MYSQL_HOST"],
            user=current_app.config["MYSQL_USER"],
            password=current_app.config["MYSQL_PASSWORD"],
            database=current_app.config["MYSQL_DATABASE"],
        )
    return g.db


def init_db():
    db = get_db()
    cursor = db.cursor()

    with current_app.open_resource("schema.sql") as f:
        sql = f.read().decode("utf-8")
        for statement in sql.split(";"):
            stmt = statement.strip()
            if stmt:
                cursor.execute(stmt)


@click.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


# Database helper functions.


def word_exists(word: str) -> bool:
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT 1 FROM words WHERE word = %s", (word,))
    return cursor.fetchone() is not None


def add_word(word, comment):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        """
        INSERT INTO words (word, comment, interval_days)
        VALUES (%s, %s, 1)
        """,
        (word, comment),
    )
    db.commit()


def update_review_date(word, interval_days):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        """
        UPDATE words
        SET interval_days = %s,
            next_review_date = DATE_ADD(CURRENT_TIMESTAMP, INTERVAL %s DAY)
        WHERE word = %s;
        """,
        (interval_days, interval_days, word),
    )
    db.commit()


def get_words_and_comments():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT word, comment FROM words;")
    words_and_comments = cursor.fetchall()
    return words_and_comments


def delete_word(word):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM words WHERE word = %s", (word,))
    db.commit()


def get_review_word_row():
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        """
        SELECT * 
        FROM words 
        WHERE next_review_date < CURRENT_TIMESTAMP 
        ORDER BY next_review_date ASC 
        LIMIT 1;
        """
    )
    row = cursor.fetchone()
    return row
