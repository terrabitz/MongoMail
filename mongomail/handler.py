import asyncio

from aiosmtpd.controller import Controller

from mongomail.utils import validate_email_addr, split_email_addr


class MongoMailHandler:
    response_error = '550 could not process email'
    response_ok = "250 OK"

    def __init__(self, connection):
        self.connection = connection

    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        _, domain = split_email_addr(address)
        if not validate_email_addr(address):
            return self.response_error
        if self.connection.check_domain(domain):
            rcpt_options.rcpt_tos.append(address)
            return self.response_ok
        else:
            return self.response_error

    async def handle_DATA(self, server, session, envelope):
        to_addresses = envelope.rcpt_to
        for to_addr in to_addresses:
            user, domain = split_email_addr(to_addr)
            if not self.connection.check_user(user, domain):
                return self.response_error
            else:
                from_addr = envelope.mail_from
                content = envelope.content.decode('utf-8')
                self.connection.add_email(from_addr=from_addr, to_addr=to_addr, body=content)

