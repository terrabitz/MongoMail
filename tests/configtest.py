import pytest

from mongomail.db.mongo import MongoConnection

@pytest.fixture
def db_handler():
    connection = MongoConnection(db_name='mongomail-test')
    yield connection
    connection.clear_db()