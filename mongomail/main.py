from flask_mongoengine import MongoEngine
from uwsgidecorators import postfork

from mongomail.rest_app import app, db

@postfork
def init_db():
    db.init_app(app)

app.run()
