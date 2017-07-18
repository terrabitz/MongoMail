"""
This file is for initializing the uWSGI application. It defines a post-fork command in
order to avoid an issue in uWSGI that prevents MongoEngine from lazily creating
mongo connections
"""

from uwsgidecorators import postfork
from mongomail.rest_app import app, db, connection


@postfork
def init_db():
    db.init_app(app)
    print("initializing db")
    if not connection.get_api_keys():
        print("No Key found")
        key = connection.generate_api_key()
        print("Generated key: " + key)
