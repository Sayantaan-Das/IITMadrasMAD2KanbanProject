import csv
import io
from flask import current_app
from jinja2 import Template
from application.models import TaskList as model_task
from application.utils.mailer import send_email
from application.utils.exceptions import NoDataFound
from application.backend_jobs.celery_system import celery
from application.cached_methods.summary_by_month import summary_by_month

@celery.task()
def task_list_report(user_id,name,email):
        current_app.logger.info("Asynchronous task to generate Task List report for User initiated!")
        try:            
            data=summary_by_month(user_id)
            if not data:
                return NoDataFound

            output = io.StringIO()
            writer = csv.writer(output)

            heading=['Task List Title, Task List Description, Number of Cards, Number of Completed Cards, Number of Incomplete Cards, Number of Incomplete Cards with overdue Deadline, Number of Cards completed within Deadline']
            writer.writerow(heading)

            for row in data:
                line=[str(row['list_title'])+','+str(row['list_description'])+','+str(row['no_cards'])+','+str(row['no_cards_completed'])+','+str(row['no_cards_incomplete'])+','+str(row['no_cards_deadline_crossed_incomplete'])+','+str(row['no_cards_completed_within_deadline'])]
                writer.writerow(line) 
                
            output.seek(0)
           
           
            with open(current_app.config["EMAIL_TEMPLATES_PATH"]+"task_list_report_email.html") as file_:
                template=Template(file_.read()).render({"name_of_user":name})
            
            send_email.apply_async([email,"Task List Report | Kanban Application",template,output.read(),"attachment_file.csv"])
            
            
            
        except Exception as e:
            current_app.logger.error(e)
  


    


