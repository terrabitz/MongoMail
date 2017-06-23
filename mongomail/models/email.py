import mongoengine
from mongoengine.fields import EmailField, StringField

class Email(mongoengine.Document):
    from_address = EmailField()
    to_address = EmailField()
    body = StringField()

    meta = {
        'collection': 'emails'
    }