from email.message import EmailMessage
import smtplib
from smtplib import SMTPRecipientsRefused
import time

import pytest

from mongomail.mail_app import controller
from mongomail.db import MongoConnection
from mongomail.utils import split_email_addr


@pytest.fixture(scope='module')
def smtpd():
    controller.start()
    yield controller
    controller.stop()


@pytest.fixture
def mail_client(smtpd):
    client = smtplib.SMTP(host=smtpd.hostname, port=smtpd.port)
    client.ehlo('pytest')
    yield client
    client.quit()


def create_msg(from_addr='asdf@asdf.com', to_addr='example@example.com', subject='This is a test',
               content='Don\t Panic'):
    msg = EmailMessage()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject
    msg.set_content(content)

    return msg


def add_test_user(handler, domain='example.com', user='example'):
    handler.add_domain(domain)
    handler.add_user(username=user, domain=domain)


# Tests #####################################################################

def test_send_valid_email(handler: MongoConnection, mail_client: smtplib.SMTP):
    add_test_user(handler)

    msg = create_msg()
    mail_client.send_message(msg)

    username, domain = split_email_addr(msg['To'])
    assert len(handler.get_emails(username=username, domain=domain)) > 0


def test_send_wrong_domain(handler: MongoConnection, mail_client: smtplib.SMTP):
    add_test_user(handler)

    msg = create_msg(to_addr='example@asdf.com')

    with pytest.raises(SMTPRecipientsRefused):
        mail_client.send_message(msg)


def test_send_bad_to_addr(handler: MongoConnection, mail_client: smtplib.SMTP):
    add_test_user(handler)

    msg = create_msg(to_addr='asdf')

    with pytest.raises(SMTPRecipientsRefused):
        mail_client.send_message(msg)
