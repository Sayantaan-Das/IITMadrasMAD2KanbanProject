from application.models import User as model_user, TaskList as model_task, Card as model_card
from application.utils.mailer import send_email
from application.utils.webhook import send_webhook
from application.backend_jobs.celery_system import celery
from jinja2 import Template
from flask import current_app

@celery.task()
def task_reminder():
    pending_cards=model_card.query.filter_by(card_status=False).all()
    print(pending_cards)
    pending_lists=[]

    for pending_card in pending_cards:
        pending_lists.append(model_task.query.filter_by(id=pending_card.card_listId).first())

    print(pending_lists)
    pending_lists_set=set(pending_lists)
    print(pending_lists_set)

    pending_users=[]
    for pending_list in pending_lists_set:
        pending_users.append(model_user.query.filter_by(id=pending_list.list_userId).first())

    print(pending_users)
    pending_users_set=set(pending_users)

    print(pending_users_set)

    try:

        for pending_user in pending_users_set:
            with open(current_app.config["EMAIL_TEMPLATES_PATH"]+"task_reminder_email.html") as file_:
                template=Template(file_.read()).render({"name_of_user":pending_user.name})

            print("action")
            
            send_email(to_address=pending_user.email,email_subject="Task Reminder | Kanban Application",email_body=template)

            if pending_user.receive_reminders_by_webhook and pending_user.webhook_url:
                send_webhook(url=pending_user.webhook_url, message={'text':'You have incomplete Cards pending. Kindly mark them complete once done!'})


    except Exception as e:
        current_app.logger.error(e)
   




