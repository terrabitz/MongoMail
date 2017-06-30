import re

from mongomail.utils import split_email_addr

class Connection:
    def add_domain(self, domain):
        raise NotImplementedError

    def add_email(self, from_addr, to_addr, content):
        raise NotImplementedError

    def add_user(self, username, domain):
        raise NotImplementedError

    def delete_domain(self, domain):
        raise NotImplementedError

    def delete_email(self, email_id):
        raise NotImplementedError

    def delete_user(self, username, domain):
        raise NotImplementedError

    def get_domain(self, domain):
        raise NotImplementedError

    def get_domains(self):
        raise NotImplementedError

    def get_emails(self, username, domain):
        raise NotImplementedError

    def get_user(self, username, domain):
        raise NotImplementedError

    def get_users(self, domain):
        raise NotImplementedError

