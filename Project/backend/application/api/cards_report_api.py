from flask import current_app
from flask_restful import Resource
from flask_security import current_user, auth_required
from application.models import TaskList as model_task
from application.backend_jobs.cards_reporter import card_report

class CardsReportAPI(Resource):
    @auth_required("token")
    def get(self, task_list_id):
        task_list=model_task.query.filter_by(id=task_list_id).first()
        if task_list.list_userId==current_user.id:
            current_app.logger.info("Card Reporter being called to generate report asynchronously!")
            card_report.apply_async([current_user.name,current_user.email,task_list_id,task_list.list_title])
            return 200
        else:
            return 404