from mongoengine import connect

from mongomail.models import Email, DomainUser, Domain
from mongomail.utils import validate_domain, validate_email_addr, split_email_addr
from ._base import Connection


class MongoConnection(Connection):
    def __init__(self, db_name, mongo_addr='127.0.0.1', mongo_port=27017, mongo_user=None, mongo_password=None):
        self.mongo_addr = mongo_addr
        self.mongo_port = mongo_port
        self.mongo_user = mongo_user
        self.mongo_password = mongo_password
        self.db_name = db_name

        connect(db=self.db_name, host=self.mongo_addr, port=self.mongo_port, username=self.mongo_user,
                password=self.mongo_password)

    def add_domain(self, domain):
        validate_domain(domain)
        if self.check_domain(domain):
            raise LookupError('Domain already exists')

        domain_object = Domain(domain=domain)
        domain_object.save()

    def add_email(self, to_addr, from_addr, content):
        validate_email_addr(to_addr)
        user, domain = split_email_addr(to_addr)
        if not self.check_user(user, domain):
            raise LookupError('User not in database')

        email = Email(from_address=from_addr, body=content)
        email.save()
        user_obj = self.get_user(username=user, domain=domain)
        user_obj.emails.append(email)
        user_obj.save()

    def add_user(self, username, domain):
        if not validate_domain(domain):
            raise ValueError('Domain not valid: {}'.format(domain))
        if self.check_user(username, domain):
            raise LookupError('User already exists in database: {}@{}'.format(username, domain))

        user_obj = DomainUser(username=username)
        user_obj.save()

        domain_object = self.get_domain(domain)
        domain_object.users.append(user_obj)
        domain_object.save()

    def check_domain(self, domain):
        valid_domains = [domain.domain for domain in Domain.objects]
        for valid_domain in valid_domains:
            if valid_domain == domain:
                return True
        else:
            return False

    def check_user(self, username, domain):
        if not self.check_domain(domain):
            return False

        domain_obj = self.get_domain(domain)
        usernames = [user.username for user in domain_obj.users]
        if not username in usernames:
            return False
        else:
            return True

    def delete_domain(self, domain):
        self.get_domain(domain).delete()

    def delete_email(self, email_id):
        Email.objects(_id=email_id).delete()

    def delete_user(self, username, domain):
        self.get_user(username, domain).delete()

    def get_domain(self, domain):
        domain_object = Domain.objects(domain=domain).first()
        return domain_object

    def get_domains(self):
        return [domain for domain in Domain.objects]

    def get_emails(self, to_addr):
        username, domain = split_email_addr(to_addr)
        user_obj = self.get_user(username, domain)
        email_list = []
        for email in user_obj.emails:
            email_list.append((email.from_address, to_addr, email.body))
        return email_list

    def get_user(self, username, domain):
        domain_obj = self.get_domain(domain)
        for user in domain_obj.users:
            if username == user:
                return user

    def get_users(self, domain):
        return [user for user in Domain.objects(domain=domain).users]

    def clear_db(self):
        [domain.delete() for domain in Domain.objects]
        [user.delete() for user in DomainUser.objects]
        [email.delete() for email in Email.objects]
