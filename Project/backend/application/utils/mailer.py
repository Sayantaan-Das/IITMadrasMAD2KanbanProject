import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from flask import current_app
from application.backend_jobs.celery_system import celery


@celery.task()
def send_email(to_address, email_subject, email_body, attachment_file_stream=None,attachment_file_name=None):
    msg=MIMEMultipart()
    msg["From"]=current_app.config["SENDER_ADDRESS"]
    msg["To"]=to_address
    msg["Subject"]=email_subject

    
    
    msg.attach(MIMEText(email_body,"html"))
   

    if attachment_file_stream:
        part=MIMEBase("application","octet-stream")
        part.set_payload(attachment_file_stream)
        encoders.encode_base64(part)
        part.add_header(
                "Content-Disposition","attachment", filename=attachment_file_name
        )
        msg.attach(part)



    s=smtplib.SMTP(host=current_app.config["SMTP_SERVER_HOST"], port=current_app.config["SMTP_SERVER_PORT"])
    s.login(current_app.config["SENDER_ADDRESS"], current_app.config["SENDER_PASSWORD"])
    s.send_message(msg)
    s.quit()


