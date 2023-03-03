from weasyprint import HTML
from jinja2 import Template
from datetime import datetime, timedelta
from application.utils.mailer import send_email
from application.models import User as model_user
from application.cached_methods.summary_by_month import summary_by_month
from application.backend_jobs.celery_system import celery
from flask import current_app
import calendar

@celery.task()
def monthly_report():
    users_list=model_user.query.filter_by().all()
    try:
        for user in users_list:
            user_summary=summary_by_month(user.id,datetime.now().date().year,datetime.now().month-1)
            if user_summary:
                with open(current_app.config["EMAIL_TEMPLATES_PATH"]+"monthly_report.html") as file_:
                    template_for_report=Template(file_.read()).render({"month":calendar.month_name[datetime.now().date().month],"name_of_user":user.name,"user_summary":user_summary})

                print("action")

                with open(current_app.config["EMAIL_TEMPLATES_PATH"]+"monthly_report_email_body.html") as file_:
                    template_for_email_body=Template(file_.read()).render({"name_of_user":user.name,"file_type":user.monthly_report_format})
                print("action")
                if user.monthly_report_format=="pdf":
                    html=HTML(string=template_for_report)
                    html.write_pdf(current_app.config["MONTHLY_REPORT_TEMPORARY_SAVE_FOLDER"]+"Monthly_Report.pdf")
                    current_app.logger.info("Pdf generated")
                    with open(current_app.config["MONTHLY_REPORT_TEMPORARY_SAVE_FOLDER"]+"Monthly_Report.pdf","rb") as file_:
                        current_app.logger.info("PDF opened")
                        send_email(to_address=user.email,email_subject="Monthly Report | Kanban Application",email_body=template_for_email_body,attachment_file_stream=file_.read(),attachment_file_name="Monthly_Report.pdf")

                else:
                        send_email.apply_async([user.email,"Monthly Report | Kanban Application",template_for_email_body,template_for_report,"Monthly_Report.html"])
        
    except Exception as e:
            current_app.logger.error(e)
            return 0

           

            


            
            

    