from flask import current_app, jsonify
from flask_restful import Resource, reqparse
from flask_security import current_user, auth_required
from application.models import TaskList as model_task
from application.backend_jobs.cards_reporter import card_report

card_request=reqparse.RequestParser()
card_request.add_argument('checked_list', action='append')


request_queue=[]
reject_queue=[]
return_string=""

class MultipleCardsReportAPI(Resource):
    @auth_required("token")
    def post(self):
        card_request_parsed=card_request.parse_args()
        current_app.logger.info(card_request_parsed.checked_list)
        current_app.logger.info(card_request_parsed)
        if len(card_request_parsed)>1:
            current_app.logger.info("Card report request for multiple Task Lists received! Each report to be mailed separately!")
        else:
            current_app.logger.info("Card report request for one Task List received!")

        for each_card in card_request_parsed.checked_list:
                if model_task.query.filter_by(id=int(each_card)).first().list_userId==current_user.id:
                    request_queue.append(int(each_card))
                else:
                    reject_queue.append(int(each_card))

        if request_queue:
                current_app.logger.info("Valid Requests Detected")
                for each_card in request_queue:
                    task_list=model_task.query.filter_by(id=each_card).first()
                    card_report.apply_async([current_user.name,current_user.email,each_card,task_list.list_title])
                current_app.logger.info("Requests scheduled asynchronously")
                return_string="Reports for valid cards scheduled to be sent to your e-mail. You should receive them shortly!"

        if reject_queue:
                return_string=return_string+" Requests rejected:"
                for each_card in reject_queue:
                    return_string=return_string+" "+str(each_card)+","

        return(jsonify({"response":return_string}))

        



