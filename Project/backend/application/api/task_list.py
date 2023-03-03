from flask import current_app
from flask_security import auth_required, current_user
from flask_restful import Resource, fields, marshal_with, reqparse
from werkzeug.exceptions import Conflict, NotFound, BadRequest, Unauthorized
from sqlalchemy.exc import IntegrityError
from application.database import db
from application.models import TaskList as model_task, Card as model_card
from application.api.cards_list import CardListAPI
from application.utils.exceptions import NoDataFound
from application.cached_data_clearer import cached_data_cleaner

task_request=reqparse.RequestParser()
task_request.add_argument('list_title', required=True, help="Name for the Task List required")
task_request.add_argument('list_description', required=True, help="Description for the Task List required")



task_request_field={
    'id': fields.Integer,
    'list_title': fields.String,
    'list_description': fields.String,
}

class TaskListAPI(Resource):

    #Method Decorators for TaskListAPI
    method_decorators = {
        'get': [marshal_with(task_request_field), auth_required('token')],
        'post': [marshal_with(task_request_field), auth_required('token')],
        'put': [marshal_with(task_request_field), auth_required('token')],
        'delete': [auth_required('token')]
    }

    #REST Methods

    
    def get(self):
            current_app.logger.info("Started fetching data of existing Task Lists for the User")
            data=model_task.query.filter_by(list_userId=current_user.id).all()
            if not data:
                current_app.logger.error("No Task Lists data found for the User")
                raise NoDataFound
            current_app.logger.info("Returning Task Lists for the User")
            return data

 
    def post(self):
        current_app.logger.info("Started parsing the request")
        data = task_request.parse_args()
        current_app.logger.info("Request data was parsed successfully")
        cached_data_cleaner(current_user.id)
        try:
            current_app.logger.info("Starting to add data to the database")
            task = model_task(**data, list_userId=current_user.id)
            db.session.add(task)
            db.session.commit()
            current_app.logger.info('Task List added to the database')
            return task
        except IntegrityError:
            current_app.logger.warning('Could not add data to database because of conflict')
            db.session.rollback()
            raise Conflict



    def put(self,id):
        if not id:
            raise BadRequest
        current_app.logger.info("Started fetching the Task List data")
        task = model_task.query.filter_by(id=id)
        if not task.first():
            current_app.logger.info("No Task List with the given id")
            raise NotFound("Data not found")
        
        if not task.first().list_userId==current_user.id:
            current_app.logger.info("The Task List doesn't belong to the current User")
            raise Unauthorized("The Task List doesn't belong to the current User")

        current_app.logger.info("Started updating the Task List")
        cached_data_cleaner(current_user.id)
        try:
            task.update(task_request.parse_args())
            db.session.commit()
        except IntegrityError:
            raise Conflict

        current_app.logger.info("Updated the Task List")

        return task.first()



    def delete(self, id=None):
        if not id:
            raise BadRequest
        current_app.logger.info("Checking if the Task List exists.")
        data = model_task.query.filter_by(id=id).first()
        if not data:
            raise NotFound("data not found")
        if not data.list_userId==current_user.id:
            current_app.logger.info("The Task List doesn't belong to the current User")
            raise Unauthorized("The Task List doesn't belong to the current User")

        cached_data_cleaner(current_user.id)
        data_card=model_card.query.filter_by(card_listId=id).all()
        if data_card:            
            current_app.logger.info("Task with id  found, deleting the cards for this list" )
            deleter=CardListAPI()
            for data_cards in data_card:
                deleter.delete(data_cards.id)
            current_app.logger.info("Deleted the cards for this list" )

        current_app.logger.info("Task with id found, deleting the data for the user")
        db.session.delete(data)
        db.session.commit()
        current_app.logger.info("Task with id  deleted by the user" )
        return ""
