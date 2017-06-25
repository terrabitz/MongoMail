import pytest

from mongomail.models import Email, Domain
from mongomail.db import MongoConnection
from mongomail.utils import split_email_addr


@pytest.fixture
def db_handler():
    connection = MongoConnection(db_name='mongomail-test')
    yield connection
    connection.clear_db()

def test_domain(db_handler: MongoConnection):
    domain = 'example.com'

    db_handler.add_domain(domain)

    inserted_obj = db_handler.get_domain(domain)
    assert inserted_obj

    db_handler.delete_domain(domain)

def test_user(db_handler: MongoConnection):
    domain = 'example.com'
    user = 'test'

    db_handler.add_domain(domain)
    db_handler.add_user(user, domain)

    user_obj = db_handler.get_user(user, domain)
    assert user_obj

    db_handler.delete_user(user, domain)

def test_email(db_handler: MongoConnection):
    from_addr = 'test@asdf.com'
    to_addr = 'test@example.com'
    content = 'This is just a test'
    user, domain = split_email_addr(to_addr)

    db_handler.add_domain(domain)
    db_handler.add_user(user, domain)
    db_handler.add_email(from_addr, to_addr, content)

    emails = db_handler.get_emails(to_addr)
    is_match = False
    for email in emails:
        if email[0] == from_addr and email[1] == to_addr and email[2] == content:
            is_match = True

    assert is_match