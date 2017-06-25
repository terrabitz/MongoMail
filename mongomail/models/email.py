from mongoengine import EmbeddedDocument
from mongoengine.fields import EmailField, StringField

class Email(EmbeddedDocument):
    from_address = EmailField()
    body = StringField()

    meta = {
        'collection': 'emails'
    }