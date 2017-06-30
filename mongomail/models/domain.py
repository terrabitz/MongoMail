from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import StringField, ReferenceField

from .email import Email


class DomainUser(Document):
    domain = ReferenceField(required=True)
    username = StringField(required=True, unique_with=domain)

class Domain(Document):
    domain = StringField(required=True, unique=True, primary_key=True)

    meta = {
        'collection': 'domains'
    }
