from mongoengine import Document
from mongoengine.fields import EmailField, StringField, ObjectIdField, ReferenceField

from .domain import DomainUser

class Email(Document):
    from_addr = EmailField()
    to_addr = EmailField()
    body = StringField(required=True)

    user_ref = ReferenceField(DomainUser, required=True)

    meta = {
        'collection': 'emails'
    }