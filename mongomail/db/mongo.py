import re

import mongoengine

from mongomail.models import Email, DomainUser, Domain

from ._base import Connection


class MongoConnection(Connection):
    def add_domain(self, domain):
        # Check if domain already in database
        domain

        domain_object = Domain(domain=domain)
        domain_object.save()
        return True

    def add_user(self, domain, username):
        domain_object = self.get_domain(domain)
        user_obj = DomainUser(username=username)
        domain_object.users.append(user_obj)
        domain_object.save()

    def add_email(self, to_addr, from_addr, content):
        self.check_user()

    def delete_domain(self, domain):
        self.get_domain(domain).delete()

    def get_domain(self, domain):
        domain_object = Domain.objects(domain=domain).first()
        return domain_object

    def check_domain(self, domain):
        valid_domains = [domain['domain'] for domain in Domain.objects]
        for valid_domain in valid_domains:
            if valid_domain == domain:
                return True
        else:
            return False

    def check_user(self, user, domain):
        if not self.check_domain(domain):
            return False

        domain_obj = self.get_domain(domain)
        usernames = [user.username for user in domain_obj.users]
        if not user in usernames:
            return False
