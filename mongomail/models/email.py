from mongoengine import Document
from mongoengine.fields import EmailField, StringField, ObjectIdField, ReferenceField

class Email(Document):
    from_address = EmailField()
    body = StringField(required=True)

    to_addr_id = ReferenceField(required=True)

    meta = {
        'collection': 'emails'
    }