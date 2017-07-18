from aiosmtpd.controller import Controller

from mongoengine import connect

from mongomail import config
from mongomail.handler import MongoMailHandler

connection = connect(config.MONGODB_DB, host=config.MONGODB_HOST, port=config.MONGODB_PORT,
                     password=config.MONGODB_PASSWORD, username=config.MONGODB_USER)

controller = Controller(MongoMailHandler(), hostname=config.MAIL_HOST, port=config.MAIL_PORT)
