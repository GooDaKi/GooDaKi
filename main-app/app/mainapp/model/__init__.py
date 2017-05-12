from .User import User
# from .Portfolio import Portfolio
# from .career import Career

from mainapp import app
from flask import g
import psycopg2

@app.before_request
def before_request():
    g.db = db = psycopg2.connect(host="main-db", database="goodaki", user="goodaki", password="goodaki")


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()