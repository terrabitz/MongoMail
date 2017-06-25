import re

DOMAIN_REGEX = '[a-zA-Z\d-]{,63}(\.[a-zA-Z\d-]{,63})*'


def split_email_addr(email_addr):
    parts = email_addr.split('@')
    if not len(parts) == 2:
        raise ValueError("Email not in proper format: " + email_addr)
    return parts[0], parts[1]


def validate_email_addr(email_addr):
    regex_string = '[a-zA-Z\d\.\-\_]+@' + DOMAIN_REGEX
    if not re.match(regex_string, email_addr):
        return False
    else:
        return True


def validate_domain(domain):
    if not re.match(DOMAIN_REGEX, domain):
        return False
    else:
        return True
