import pytest

from mongomail.db import MongoConnection
from mongomail.utils import split_email_addr


def test_domain(handler: MongoConnection):
    domain = 'example.com'

    handler.add_domain(domain)

    inserted_obj = handler.get_domain(domain)
    assert inserted_obj

    handler.delete_domain(domain)

def test_user(handler: MongoConnection):
    domain = 'example.com'
    username = 'test'

    handler.add_domain(domain)
    handler.add_user(username, domain)

    user_obj = handler.get_user(username, domain)
    assert user_obj

    handler.delete_user(username, domain)

def test_email(handler: MongoConnection):
    from_addr = 'test@asdf.com'
    to_addr = 'test@example.com'
    body = 'This is just a test'
    username, domain = split_email_addr(to_addr)

    handler.add_domain(domain)
    handler.add_user(username, domain)
    handler.add_email(to_addr=to_addr, from_addr=from_addr, body=body)

    emails = handler.get_emails(username=username, domain=domain)
    has_match = False
    for email in emails:
        if email.from_addr == from_addr and email.to_addr == to_addr and email.body == body:
            has_match = True

    assert has_match