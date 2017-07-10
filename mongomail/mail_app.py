from aiosmtpd.controller import Controller

from mongoengine import connect

from mongomail import config
from mongomail.handler import MongoMailHandler

connection = connect(config.MONGO_DB, host=config.MONGO_HOST, port=config.MONGO_PORT,
                     password=config.MONGO_PASSWORD, username=config.MONGO_USER)
controller = Controller(MongoMailHandler(), hostname=config.MAIL_HOST, port=config.MAIL_PORT)
