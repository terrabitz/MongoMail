import pytest

from mongomail.db import MongoConnection
from mongomail.utils import split_email_addr


def test_domain(db_handler: MongoConnection):
    domain = 'example.com'

    db_handler.add_domain(domain)

    inserted_obj = db_handler.get_domain(domain)
    assert inserted_obj

    db_handler.delete_domain(domain)

def test_user(db_handler: MongoConnection):
    domain = 'example.com'
    username = 'test'

    db_handler.add_domain(domain)
    db_handler.add_user(username, domain)

    user_obj = db_handler.get_user(username, domain)
    assert user_obj

    db_handler.delete_user(username, domain)

def test_email(db_handler: MongoConnection):
    from_addr = 'test@asdf.com'
    to_addr = 'test@example.com'
    body = 'This is just a test'
    username, domain = split_email_addr(to_addr)

    db_handler.add_domain(domain)
    db_handler.add_user(username, domain)
    db_handler.add_email(to_addr=to_addr, from_addr=from_addr, body=body)

    emails = db_handler.get_emails(username=username, domain=domain)
    has_match = False
    for email in emails:
        if email.from_addr == from_addr and email.to_addr == to_addr and email.body == body:
            has_match = True

    assert has_match