from mongomail.rest_app import app, db

if __name__ == '__main__':
    db.init_app(app)
    app.run('0.0.0.0', port=8000)