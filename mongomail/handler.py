class MongoMailHandler:
    response_error = '550 could not process email'
    response_ok = "250 OK"

    def __init__(self, mongo_addr='localhost', mongo_port=27017, mongo_user=None, mongo_password=None,
                 db_name='mongomail'):
        self.mongo_addr = mongo_addr
        self.mongo_port = mongo_port
        self.mongo_user = mongo_user
        self.mongo_password = mongo_password
        self.db_name = db_name
        connect(db=self.db_name, host=self.mongo_addr, port=self.mongo_port, username=self.mongo_user,
                password=self.mongo_password)

    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        if not '@' in address:
            return self.response_error
        to_domain = address.split('@')[-1]
        if self.check_domain(to_domain):
            rcpt_options.rcpt_tos.append(address)
            return self.response_ok
        return self.response_error

    async def handle_DATA(self, server, session, envelope):
        to_addresses = envelope.rcpt_to
        for to_address in to_addresses:
            if not self.check_domain(to_address.split('@')[-1]):
                return self.response_error


        email = Email(from_address=envelope.mail_from, to_address)

