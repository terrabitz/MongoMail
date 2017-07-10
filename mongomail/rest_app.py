from bson import ObjectId
import traceback
import json

from flask import Flask
from flask_mongoengine import MongoEngine
from flask_restful import Resource, Api
from mongoengine.errors import DoesNotExist, NotUniqueError

from mongomail.db.mongo import MongoConnection

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = MongoEngine()
api = Api(app)
connection = MongoConnection()

ERROR_RESPONSE = {'status': 'error', 'error': 'An error occured'}, 500
NOT_FOUND_RESPONSE = {'status': 'error', 'error': 'The resource does not exist'}, 404
DUPLICATE_RESPONSE = {'status': 'error', 'error': 'The resource already exists'}, 404
SUCCESS_RESPONSE = {'status': 'success'}


def nice_errors(func):
    def _redirect_on_error(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
            if not response:
                response = SUCCESS_RESPONSE
            elif isinstance(response, dict):
                response.update(**SUCCESS_RESPONSE)
            return response
        except NotUniqueError:
            return DUPLICATE_RESPONSE
        except DoesNotExist:
            return NOT_FOUND_RESPONSE
        except Exception as e:
            traceback.print_exc()
            return ERROR_RESPONSE

    return _redirect_on_error

@app.errorhandler(404)
def page_not_found(e):
    return NOT_FOUND_RESPONSE

class Users(Resource):
    @nice_errors
    def get(self, username, domain):
        user_obj = connection.get_user(username=username, domain=domain)
        return {'username': user_obj.username, 'domain': user_obj.domain.domain}

    @nice_errors
    def put(self, username, domain):
        connection.add_user(username=username, domain=domain)
        return {}

    @nice_errors
    def delete(self, username, domain):
        connection.delete_user(username=username, domain=domain)
        return {}


class Domain(Resource):
    @nice_errors
    def get(self, domain):
        domain_obj = connection.get_domain(domain)
        return {'domain': domain_obj.domain}

    @nice_errors
    def put(self, domain):
        connection.add_domain(domain)
        return {}

    @nice_errors
    def delete(self, domain):
        connection.delete_domain(domain)
        return {}


class AllDomains(Resource):
    @nice_errors
    def get(self):
        domain_objs = connection.get_domains()
        ret_val = [domain_obj.domain for domain_obj in domain_objs]
        return {'domains': ret_val}


class AllUsers(Resource):
    @nice_errors
    def get(self, domain):
        user_objs = connection.get_users(domain)
        ret_val = [user_obj.username for user_obj in user_objs]
        return {'users': ret_val}


class AllEmails(Resource):
    @nice_errors
    def get(self, domain, username):
        email_objs = connection.get_emails(username, domain)
        ret_val = []
        for email_obj in email_objs:
            mail_id = str(email_obj.id)
            mail_tuple = {'from': email_obj.from_addr, 'to': email_obj.to_addr, 'body': email_obj.body,
                          'id': mail_id}
            ret_val.append(mail_tuple)

        return {'emails': ret_val}


class Email(Resource):
    @nice_errors
    def get(self, email_id):
        email_id_bson = ObjectId(email_id)
        email_obj = connection.get_email(email_id_bson)
        return {'from': email_obj.from_addr,
                'to': email_obj.to_addr,
                'body': email_obj.body,
                'id': email_id}

    @nice_errors
    def delete(self, email_id):
        email_id_bson = ObjectId(email_id)
        connection.delete_email(email_id_bson)


@app.route("/")
def index():
    return json.dumps({'status': 'success'})




api.add_resource(AllDomains, '/domains')
api.add_resource(Email, '/emails/<string:email_id>')
api.add_resource(Domain, '/<string:domain>')
api.add_resource(AllUsers, '/<string:domain>/users')
api.add_resource(Users, '/<string:domain>/<string:username>')
api.add_resource(AllEmails, '/<string:domain>/<string:username>/emails')
