from flask_restful import Api
from application.api.user import *
from application.api.task_list import *
from application.api.cards_list import *
from application.api.summary import *
from application.api.task_list_report_api import *
from application.api.trendline_api import *
from application.api.cards_report_api import *
from application.api.multiple_cards_report_api import *
from application.api.import_task_list_api import *
from application.api.download_csv import *
from application.api.move_card import *

api=Api()


api.add_resource(UserAPI, "/api/user")
api.add_resource(TaskListAPI, "/api/task", "/api/task/<int:id>")
api.add_resource(CardListAPI, "/api/card", "/api/card/<int:id>")
api.add_resource(MoveCard,"/api/movecard", "/api/movecard/<int:id>")
api.add_resource(SummaryAPI, "/api/summary")
api.add_resource(TaskListReportAPI, "/api/tasklistreport")
api.add_resource(CardsReportAPI, "/api/cardsreport/<int:task_list_id>")
api.add_resource(MultipleCardsReportAPI,"/api/multiplecardsreport")
api.add_resource(TrendlineAPI, "/api/trendline/<int:list_id>")
api.add_resource(DownloadCSVTemplateAPI,"/api/downloadcsvtemplate")
api.add_resource(ImportTaskListAPI,"/api/importtasklist")
