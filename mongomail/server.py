import configparser

from aiosmtpd.controller import Controller

from mongomail.handler import MongoMailHandler
from mongomail.db import MongoConnection

db_name = 'mongomail'

connection = MongoConnection(db_name=db_name)
controller = Controller(MongoMailHandler(connection))

