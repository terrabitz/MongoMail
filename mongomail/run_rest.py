from mongomail import config

from mongomail.rest_app import app
from flask_mongoengine import MongoEngine

if __name__ == '__main__':
    app.db = MongoEngine()
    app.db.init_app(app)
    app.run('0.0.0.0', port=8000)
