from mongoengine import Document
from mongoengine.fields import StringField

class DomainUsers(Document):
    username = StringField()

class Domain(Document):
    domain = StringField()
