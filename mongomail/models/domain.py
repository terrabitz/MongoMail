from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import StringField, ListField, ReferenceField, EmbeddedDocumentField

from .email import Email

class DomainUser(EmbeddedDocument):
    username = StringField(required=True)
    emails = ListField(EmbeddedDocumentField(Email))

class Domain(Document):
    domain = StringField(required=True, unique=True)
    users = ListField(EmbeddedDocumentField(DomainUser))

    meta = {
        'collection': 'domains'
    }
