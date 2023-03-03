from flask import current_app
from flask_restful import Resource
from flask_security import current_user, auth_required
from application.backend_jobs.task_list_reporter import task_list_report

class TaskListReportAPI(Resource):
    @auth_required("token")
    def get(self):
        current_app.logger.info("Task List Reporter being called to generate report asynchronously!")
        task_list_report.apply_async([current_user.id,current_user.name,current_user.email])
        return 200