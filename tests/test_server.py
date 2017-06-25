import pytest
from mongoengine import connect

from mongomail.models import Email, Domain
from mongomail.server import MongoMailHandler


@pytest.fixture(scope='module')
def mongo_mail_handler():
    return MongoMailHandler(db_name='mongomail-test')


@pytest.fixture
def email():
    return None


def test_add_domain(mongo_mail_handler):
    domain = 'example.com'

    mongo_mail_handler.add_domain(domain)
    db_entry = Domain.objects(domain=domain)
    assert db_entry
    db_entry.delete()


def test_delete_domain(mongo_mail_handler):
    domain = 'example.com'

    Domain(domain=domain).save()
    mongo_mail_handler.delete