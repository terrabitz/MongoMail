from mongomail.rest_app import app, db, connection

if __name__ == '__main__':
    db.init_app(app)
    if not connection.get_api_keys():
        print("No Key found")
        key = connection.generate_api_key()
        print("Generated key: " + key)
    app.run('0.0.0.0', port=8000)
