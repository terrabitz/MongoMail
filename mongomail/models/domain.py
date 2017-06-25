from mongoengine import Document
from mongoengine.fields import StringField, ListField, ReferenceField

from .email import Email

class DomainUser(Document):
    username = StringField(required=True)
    emails = ListField(ReferenceField(Email))

class Domain(Document):
    domain = StringField(required=True, unique=True)
    users = ListField(ReferenceField(DomainUser))

    meta = {
        'collection': 'domains'
    }
