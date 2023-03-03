from json import dumps
from httplib2 import Http
from flask import current_app
from application.backend_jobs.celery_system import celery

@celery.task()
def send_webhook(url,message):
    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
    http_obj = Http()
    response = http_obj.request(
        uri=url,
        method='POST',
        headers=message_headers,
        body=dumps(message),
    )

    current_app.logger.info(response)



