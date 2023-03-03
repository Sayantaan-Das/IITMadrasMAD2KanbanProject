from datetime import datetime
from flask import current_app
from flask_restful import Resource, marshal_with, reqparse, fields
from flask_security import current_user, auth_required
from werkzeug.exceptions import Unauthorized
from application.database import db
from application.models import TaskList as model_task, Card as model_card
from application.utils.exceptions import NoDataFound
from application.cached_methods.is_authorized_for_card import is_authorized_for_the_card
from application.cached_data_clearer import cached_data_cleaner

card_change_list=reqparse.RequestParser()
card_change_list.add_argument('card_id', required=True, help="ID of the Card of which the Task List has to be changed")
card_change_list.add_argument('update_to_list_id', required=True, help="Task List ID to which the Card has to be updated required")

valid_lists={
    'title': fields.String,
    'id': fields.Integer
}
valid_list_for_change_response={
    'current_list_title': fields.String,
    'list_of_valid_list': fields.List(fields.Nested(valid_lists))
}

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

class MoveCard(Resource):
    method_decorators = {
        'get': [marshal_with(valid_list_for_change_response), auth_required('token')],
        'put': [marshal_with(card_request_field), auth_required('token')],
    }

    def get(self,id):
        current_app.logger.info("Request to change the Task List of a Card received")
        card=model_card.query.filter_by(id=id)
        if card:
            if (is_authorized_for_the_card(id, current_user.id)):
                task_list=model_task.query.filter_by(list_userId=current_user.id).all()
                current_app.logger.info("Here")
                response={
                    'current_list_title': model_task.query.filter_by(id=card.first().card_listId).first().list_title,  
                }
                valid_task_list_id=[]
                for each_task_list in task_list:
                    if each_task_list.id!=card.first().card_listId:
                        valid_task_list_id.append({"title":each_task_list.list_title,"id":each_task_list.id})

                response['list_of_valid_list']=valid_task_list_id

                return response
        else:
            NoDataFound
                        




    def put(self):
        current_app.logger.info("Request to change the Task List of a Card received.")
        card_change_list_parsed=card_change_list.parse_args()
        card=model_card.query.filter_by(id=card_change_list_parsed.card_id)
        current_app.logger.info("Card Found.")
        if card:
            if (is_authorized_for_the_card(card_change_list_parsed.card_id,current_user.id)) and ((model_task.query.filter_by(id=card_change_list_parsed.update_to_list_id).first().list_userId)==current_user.id):
                cached_data_cleaner(user_id=current_user.id,task_list_id=card.first().card_listId)
                cached_data_cleaner(user_id=current_user.id,task_list_id=card_change_list_parsed.update_to_list_id)
                card.first().card_listId=card_change_list_parsed.update_to_list_id
                card.first().card_last_updated=datetime.now()
                db.session.commit()
                return card
            else:
                current_app.logger.info("The User does not have access to either the Card or the Task List to which the User is trying to assing the Card.")
                raise Unauthorized
        else:
            current_app.logger.info("No Card found!")
            raise NoDataFound


