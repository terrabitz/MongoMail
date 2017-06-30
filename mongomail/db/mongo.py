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
        if not validate_domain(domain):
            raise ValueError('Domain not valid')
        domain_object = Domain(domain=domain)
        domain_object.save()

    def add_email(self, to_addr, from_addr, body):
        if not validate_email_addr(to_addr):
            raise ValueError('To Address not valid: ' + to_addr)
        user, domain = split_email_addr(to_addr)
        user_obj = self.get_user(username=user, domain=domain)
        email = Email(from_addr=from_addr, to_addr=to_addr, body=body, user_ref=user_obj)
        email.save()

    def add_user(self, username, domain):
        if not validate_domain(domain):
            raise ValueError('Domain not valid: {}'.format(domain))

        domain_obj = self.get_domain(domain)
        user_obj = DomainUser(username=username, domain=domain_obj)
        user_obj.save()

    def delete_domain(self, domain):
        self.get_domain(domain).delete()

    def delete_email(self, email_id):
        self.get_email(email_id).delete()

    def delete_user(self, username, domain):
        self.get_user(username, domain).delete()

    def get_domain(self, domain):
        return Domain.objects(domain=domain).get()

    def get_domains(self):
        return Domain.objects

    def get_email(self, email_id):
        return Email.objects(_id=email_id).get()

    def get_emails(self, username, domain):
        user_obj = self.get_user(username, domain)
        return Email.objects(user_ref=user_obj)

    def get_user(self, username, domain):
        domain_obj = self.get_domain(domain)
        return DomainUser.objects(username=username, domain=domain_obj).get()

    def get_users(self, domain):
        domain_obj = self.get_domain(domain)
        return DomainUser.objects(domain=domain_obj)

    def clear_db(self):
        DomainUser.drop_collection()
        Domain.drop_collection()
        Email.drop_collection()

