import random
import string
from datetime import date
from flask import current_app
from flask_restful import Resource
from flask_restful import fields, marshal_with
from flask_restful import reqparse
from flask_security import auth_required, current_user, hash_password
from jinja2 import Template
from sqlalchemy.exc import IntegrityError
from application.database import db
from werkzeug.exceptions import Conflict, Unauthorized
from application.models import User as model_user
from application.utils.mailer import send_email
from application.utils.security import user_datastore
from application.utils.exceptions import NoDataFound


user_request_get=reqparse.RequestParser()
user_request_get.add_argument('email', required=True, help="Email required")
user_request_get.add_argument('password', required=True, help="Password required")
user_request_get.add_argument('name', required=True, help="Name required")

user_request_put=reqparse.RequestParser()
user_request_put.add_argument('monthly_report_format')
user_request_put.add_argument('receive_reminders_by_webhook',type=bool)
user_request_put.add_argument('webhook_url')

user_request_field={
    'name': fields.String,
    'email': fields.String,
    'created': fields.DateTime(dt_format='iso8601'),
    'monthly_report_format': fields.String,
    'receive_reminders_by_webhook': fields.Boolean,
    'webhook_url': fields.String
}

class UserAPI(Resource):

    #Method Decorators for UserAPI
    method_decorators = {
        'get': [marshal_with(user_request_field), auth_required('token')],
        'post': [marshal_with(user_request_field)],
        'put': [marshal_with(user_request_field), auth_required('token')]
    }

    #REST Methods

    def get(self):
        current_app.logger.info("Searching for user to start now.")
        data=model_user.query.filter_by(id=current_user.id).first()
        if data:
            current_app.logger.info("User found! Returning details of the User.")
            return data
        else:
            current_app.logger.info("Unable to find the User!")
            raise NoDataFound
        

    def post(self):
        current_app.logger.info('Started Parsing User Creation Request')
        data = user_request_get.parse_args()
        current_app.logger.info('request parsed')
        if user_datastore.find_user(email=data['email']):
            raise Conflict
        try:
            current_app.logger.info('started creating user in database')
            user = user_datastore.create_user(
                email=data['email'],
                password=hash_password(data['password']),
                name = data['name'],
                created = date.today(),
                fs_uniquifier = str(''.join(random.choices(string.ascii_uppercase + string.digits, k=12))))
            db.session.commit()
            current_app.logger.info('inserted the data in database')

            current_app.logger.info('Asynchronous Task to send welcome email initiated')

            with open(current_app.config["EMAIL_TEMPLATES_PATH"]+"welcome_email.html") as file_:
                template=Template(file_.read()).render({"user_name":data['name']})
            
            send_email.apply_async([data['email'],"Welcome | Kanban Application",template])

            return user
        except IntegrityError:
            raise Conflict


    def put(self):
        current_app.logger.info("Searching for user to start now.")
        user=model_user.query.filter_by(id=current_user.id)
        if user.first():
            try:
                current_app.logger.info("User found. Starting parsing request now.")
                data = user_request_put.parse_args()
                #if data["receive_reminders_by_webhook"]=="true":
                    #data["receive_reminders_by_webhook"]=True
                #else:
                    #data["receive_reminders_by_webhook"]=False

                user.update(data)
                db.session.commit()
                return user.first()
            except IntegrityError:
                raise Conflict
        else:
            Unauthorized
