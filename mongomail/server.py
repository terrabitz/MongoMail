import re
import asyncio

from aiosmtpd.controller import Controller
from raven import Client
from mongoengine import connect

from .models.email import Email


class MongoMailServer:
    def __init__(self, mongo_addr='localhost', mongo_port=27017, mongo_user=None, mongo_password=None,
                 db_name='mongomail', srv_addr='127.0.0.1', srv_port=25, domains=None):
        self.mongo_addr = mongo_addr
        self.mongo_port = mongo_port
        self.mongo_user = mongo_user
        self.mongo_password = mongo_password
        self.srv_addr = srv_addr
        self.srv_port = srv_port
        self.db_name = db_name

        if not domains:
            domains = {}

        self.domains = domains
        self.connection = connect(db_name, host=self.mongo_addr, port=self.mongo_port, username=self.mongo_user,
                                  password=self.mongo_password)
        self.controller = Controller(MongoMailHandler(self.domains))

    def add_domain(self, domain):
        regex_string = '[a-zA-Z\d-]{,63}(\.[a-zA-Z\d-]{,63})*'
        if not re.match(regex_string, domain):
            return False

        self.domains[domain] = []
        return True

    def delete_domain(self, domain):
        result = self.domains.pop(domain, None)
        if not result:
            return False

        return True

    def add_user(self, domain, username):
        if domain not in self.domains.keys():
            raise KeyError("Domain name not found")
        else:
            pass


class MongoMailHandler:
    def __init__(self, domains):
        self.domains = domains

    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):

        to_domains = [addr.split('@')[-1] for addr in envelope.rcpt_tos]

        for to_domain in to_domains:
            for domain in self.domains:
                if to_domain == domain:
                    return '250 OK'
        return '550 could not process email'

    async def handle_DATA(self, server, session, envelope):
        pass


if __name__ == '__main__':
    pass
