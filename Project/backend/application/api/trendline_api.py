from flask import jsonify
from flask_security import auth_required, current_user
from flask_restful import Resource
from application.models import TaskList as model_task
from application.cached_methods.trendline import generate_trendline_completed
from application.utils.exceptions import NoDataFound

class TrendlineAPI(Resource):
    @auth_required("token")
    def get(self,list_id):
        if model_task.query.filter_by(id=list_id).first().list_userId==current_user.id:
            return jsonify({"base64_encoded_image":generate_trendline_completed(list_id)})
        else:
            raise NoDataFound
        


