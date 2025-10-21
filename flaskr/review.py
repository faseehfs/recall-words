from .db import get_db


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
