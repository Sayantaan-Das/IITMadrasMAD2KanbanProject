from flask import Flask
from application.database import db
from application.api import api
from application.utils.cache_system import cache
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from application.utils.error_handler import generic_error_handler, http_exception_handler
from application.utils.security import user_datastore, sec
from application.backend_jobs.celery_system import celery, ContextTask
from application.backend_jobs.periodic_tasks import *
from application.utils.webhook import *

app=None


def create_app(config):
    app=Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    sec.init_app(app,user_datastore)
    app.app_context().push()
    api.init_app(app)

    app.register_error_handler(Exception, generic_error_handler)
    app.register_error_handler(HTTPException, http_exception_handler)

    celery.conf.update(
        broker_url=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["CELERY_RESULT_BACKEND"],
        timezone=app.config["TIMEZONE"],
        enable_utc=False)

    celery.Task=ContextTask

    app.app_context().push()

    cache.init_app(app)
    app.app_context().push()


    CORS(app, resources={r'/*': {'origins': '*'}})

    return app, api, celery, cache