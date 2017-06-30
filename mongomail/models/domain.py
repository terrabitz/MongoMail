from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import StringField, ReferenceField


class Domain(Document):
    domain = StringField(required=True, unique=True)

    meta = {
        'collection': 'domains'
    }


class DomainUser(Document):
    domain = ReferenceField(Domain, required=True)
    username = StringField(required=True, unique_with='domain')
