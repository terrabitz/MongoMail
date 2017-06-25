import re


class Connection:
    @staticmethod
    def split_email_addr(email_addr):
        parts = email_addr.split('@')
        if not len(parts) == 2:
            raise ValueError("Email not in proper format: " + email_addr)
        return parts[0], parts[1]

    @staticmethod
    def validate_email(self, email_addr):
        pass

    @staticmethod
    def validate_domain(self, domain):
        regex_string = '[a-zA-Z\d-]{,63}(\.[a-zA-Z\d-]{,63})*'
        if not re.match(regex_string, domain):
            return False
        return True

    def check_email_addr(self, email_addr):
        username, domain = self.split_email_addr(email_addr)
        return self.check_user(username=username, domain=domain)

    def get_domain(self, domain):
        raise NotImplementedError

    def get_user(self, username, domain):
        raise NotImplementedError

    def get_emails(self, to_addr):
        raise NotImplementedError

    def check_domain(self, domain):
        raise NotImplementedError

    def check_user(self, username, domain):
        raise NotImplementedError

    def add_domain(self, domain):
        raise NotImplementedError

    def add_user(self, username, domain):
        raise NotImplementedError

    def _add_email(self, from_addr, to_addr, content):


    def add_email(self, from_addr, to_addr, content):
        raise NotImplementedError
