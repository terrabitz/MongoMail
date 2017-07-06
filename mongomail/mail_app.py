from aiosmtpd.controller import Controller

from mongomail.handler import MongoMailHandler
from mongomail.db.mongo import MongoConnection

from mongomail import config

connection = MongoConnection(db_name=config.MONGO_DB, mongo_addr=config.MONGO_HOST, mongo_port=config.MONGO_PORT,
                             mongo_password=config.MONGO_PASSWORD, mongo_user=config.MONGO_USER)
controller = Controller(MongoMailHandler(connection), hostname=config.MAIL_HOST, port=config.MAIL_PORT)
