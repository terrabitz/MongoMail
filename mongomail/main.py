from uwsgidecorators import postfork
from mongomail.rest_app import app, db

@postfork
def init_db():
    print("initializing db")
    db.init_app(app)
