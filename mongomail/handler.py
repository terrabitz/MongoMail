import asyncio

from mongomail.utils import validate_email_addr, split_email_addr
from mongomail.db.mongo import MongoConnection

connection = MongoConnection()

class MongoMailHandler:
    response_error = '550 could not process email'
    response_ok = "250 OK"

    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        username, domain = split_email_addr(address)
        try:
            if not validate_email_addr(address):
                return self.response_error
            if connection.get_user(username, domain):
                envelope.rcpt_tos.append(address)
                return self.response_ok
        except:
            return self.response_error

    async def handle_DATA(self, server, session, envelope):
        try:
            to_addresses = envelope.rcpt_tos
            for to_addr in to_addresses:
                user, domain = split_email_addr(to_addr)
                if connection.get_user(user, domain):
                    from_addr = envelope.mail_from
                    content = envelope.content.decode('utf-8')
                    connection.add_email(from_addr=from_addr, to_addr=to_addr, body=content)
            return self.response_ok
        except:
            return self.response_error
