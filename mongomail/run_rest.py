from mongomail import config

from mongomail.rest_app import app
from mongomail.db.mongo import MongoConnection

if __name__ == '__main__':
    connection = MongoConnection(db_name=config.MONGO_DB, mongo_addr=config.MONGO_HOST, mongo_port=config.MONGO_PORT,
                                 mongo_password=config.MONGO_PASSWORD, mongo_user=config.MONGO_USER)
    app.connection = connection
    app.run('0.0.0.0', port=80)
