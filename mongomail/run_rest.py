from flask_mongoengine import MongoEngine

from mongomail.rest_app import app

def main():
    db = MongoEngine()
    db.init_app(app)
    app.run('0.0.0.0', port=8000)

if __name__ == '__main__':
    main()