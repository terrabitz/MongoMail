import random
import string

from mongoengine import Document
from mongoengine.fields import StringField

KEY_SIZE = 32


class ApiKey(Document):
    key = StringField(required=True, unique=True,
                      default=''.join([random.choice(string.ascii_letters + string.digits) for _ in range(KEY_SIZE)]))
