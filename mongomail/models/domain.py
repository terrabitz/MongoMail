from mongoengine import Document
from mongoengine.fields import StringField, ListField

class Domain(Document):
    domain = StringField()
    users = ListField(StringField())

    meta={
        'collection': 'domains'
    }