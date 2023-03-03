from flask_restful import Resource
from flask_security import current_user, auth_required
from flask import current_app
from application.cached_methods.summary_by_month import summary_by_month


class SummaryAPI(Resource):
    @auth_required("token")
    def get(self):
        current_app.logger.info("Summary API Reached. Calling summary function!")
        summary = summary_by_month(current_user.id)
        return summary









