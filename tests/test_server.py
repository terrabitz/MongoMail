import pytest

from mongomail.server import MongoMailServer

@pytest.fixture(scope='module')
def mongo_mail_server():
    return MongoMailServer()

@pytest.fixture
def test_email():
    return None