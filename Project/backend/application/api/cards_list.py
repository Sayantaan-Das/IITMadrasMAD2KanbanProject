from flask import current_app
from flask_security import auth_required, current_user
from flask_restful import Resource
from flask_restful import fields, marshal_with
from flask_restful import reqparse
from datetime import datetime, timezone
from werkzeug.exceptions import Conflict, NotFound, BadRequest, Unauthorized
from sqlalchemy.exc import IntegrityError
from application.database import db
from application.models import Card as model_card, TaskList as model_task
from application.utils.exceptions import NoDataFound
from application.cached_data_clearer import cached_data_cleaner
from application.cached_methods.is_authorized_for_card import is_authorized_for_the_card



card_request=reqparse.RequestParser()
card_request.add_argument('card_listId', required=True, help="List ID missing")
card_request.add_argument('card_title', required=True, help="Card Title missing")
card_request.add_argument('card_content', required=True, help="Card Content missing")
card_request.add_argument('card_deadline', required=True, help="Card deadline missing")
card_request.add_argument('card_status')


card_request_field={
    'id': fields.Integer,
    'card_listId': fields.Integer,
    'card_title': fields.String,
    'card_content': fields.String,
    'card_deadline': fields.DateTime(dt_format='iso8601'),
    'card_status': fields.Boolean,
    'card_completed_on': fields.DateTime(dt_format='iso8601'),
    'card_completed_within_deadline': fields.Boolean,
    'card_last_updated': fields.DateTime(dt_format='iso8601')
}







class CardListAPI(Resource):

    #Method Decorators for CardListAPI
    method_decorators = {
        'get': [marshal_with(card_request_field), auth_required('token')],
        'post': [marshal_with(card_request_field), auth_required('token')],
        'put': [marshal_with(card_request_field), auth_required('token')],
        'delete': [auth_required('token')]
    }

    #REST Methods



    def get(self, id=None):
        if not id:
            raise BadRequest
        current_app.logger.info("Started fetching data for the list ID ")

        if(model_task.query.filter_by(id=id).first().list_userId==current_user.id):
            data=model_card.query.filter_by(card_listId=id).all()
            if not data:
                current_app.logger.error("No cards found for List ID")
                raise NoDataFound
            current_app.logger.info("returning cards for the list ID ")
            return data
        else:
            raise Unauthorized


 
    def post(self):
        current_app.logger.info('started parsing request')
        data = card_request.parse_args()
        current_app.logger.info('request data was parsed successfully')
        if model_task.query.filter_by(id=data.card_listId).first().list_userId==current_user.id:
            try:
                cached_data_cleaner(user_id=current_user.id,task_list_id=int(data.card_listId))
                current_app.logger.info('Starting to add data in data base')
                card = model_card(**data)
                db.session.add(card)
                db.session.commit()
                current_app.logger.info('Card added to the database')
                return card
            except IntegrityError:
                current_app.logger.warning('Could not add data to database because of conflict')
                db.session.rollback()
                raise Conflict
        else:
            raise Unauthorized



    def put(self, id=None):
        if not id:
            raise BadRequest
        card_request_parsed=card_request.parse_args()
        current_app.logger.info("Started fetching the Card data")
        if (is_authorized_for_the_card(id,current_user.id)):
            card = model_card.query.filter_by(id=id)
            if not card.first():
                current_app.logger.info("No Card with the given id")
                raise NoDataFound

            current_app.logger.info("Started updating the card")
            cached_data_cleaner(user_id=current_user.id,task_list_id=int(card_request_parsed.card_listId),card_id=id)
            try:
                temp=datetime.strptime(card_request_parsed.card_deadline, "%Y-%m-%dT%H:%M:%S.%fZ")
                card_request_parsed.card_deadline=temp
                
                card_request_parsed.card_status=True if (card_request_parsed.card_status=="true") else False
                if card_request_parsed.card_status and not card.first().card_status:
                    card_request_parsed["card_completed_on"]=datetime.now()
                    if card_request_parsed.card_deadline>=datetime.strptime(datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),"%Y-%m-%dT%H:%M:%S.%fZ"):
                        card_request_parsed["card_completed_within_deadline"]=True
                if not card_request_parsed.card_status and card.first().card_status:
                    card_request_parsed["card_completed_on"]=None
                    card_request_parsed["card_completed_within_deadline"]=False
                
                card_request_parsed["card_last_updated"]=datetime.now()
                card.update(card_request_parsed)
                db.session.commit()
            except IntegrityError:
                raise Conflict
            current_app.logger.info("Updated the task with id  for user ")

            return card.first()



    def delete(self, id=None):
        if not id:
            raise BadRequest
        if is_authorized_for_the_card(id,current_user.id):
            current_app.logger.info('Checking if task with id exist')
            data = model_card.query.filter_by(id=id).first()
            if not data:
                raise NotFound("data not found")

            cached_data_cleaner(user_id=current_user.id,task_list_id=data.card_listId, card_id=id)
            current_app.logger.info("Task with id found, deleting the data for the user")
            db.session.delete(data)
            db.session.commit()
            current_app.logger.info("Task with id deleted by the user" )
            return ""