# Recall Words

## Default Config

```python
SECRET_KEY="dev",
MYSQL_HOST="localhost",
MYSQL_USER="recall_words_user",
MYSQL_PASSWORD="recall_words_password",
MYSQL_DATABASE="recall_words_db",
```

## Response Standards

-   GET requests: returns a web page.
-   POST requests:
    -   For success: returns json.
    -   For error: returns json with a "message" field, which is often alerted in the frontend (status code 400).
