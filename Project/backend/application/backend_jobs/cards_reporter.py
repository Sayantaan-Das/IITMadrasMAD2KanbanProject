import csv
import io
from datetime import timedelta
from flask import current_app
from application.models import Card as model_card
from application.utils.mailer import send_email
from jinja2 import Template
from application.backend_jobs.celery_system import celery

@celery.task()
def card_report(user_name,email,list_id,task_list_name):
        current_app.logger.info("Asynchronous task to generate Task List report for User initiated!")
        try:            
            data=model_card.query.filter_by(card_listId=list_id).all()
            if not data:
                return 0

            output = io.StringIO()
            writer = csv.writer(output)

            heading=['Card Title, Card Content, Card Deadline, Card Completed?, Card Completed On']
            writer.writerow(heading)

            for row in data:
                row=vars(row)
                line=[str(row['card_title'])+','+str(row['card_content'])+','+str(row['card_deadline']+timedelta(hours=5,minutes=30))+','+str(row['card_status'])+','+str(row['card_completed_on'])]
                writer.writerow(line) 
                
            output.seek(0)
           
           
            with open(current_app.config["EMAIL_TEMPLATES_PATH"]+"card_report_email.html") as file_:
                template=Template(file_.read()).render({"name_of_user":user_name,"task_list_name":task_list_name})
            
            send_email.apply_async([email,"Cards Report | Kanban Application",template,output.read(),"attachment_file.csv"])
            
            
            
        except Exception as e:
            current_app.logger.error(e)
 


    


