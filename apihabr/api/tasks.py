from apihabr.celery import app

from .parser_logic import insert_db


@app.task
def сelery_insert_db():
    insert_db()


@app.task
def celery_parse_habr_everyday():
    insert_db()
