from flask import current_app
import pandas
from application.models import TaskList as model_task
from application.database import db
from application.backend_jobs.celery_system import celery



@celery.task()
def import_task_list(user_id,file_path):

      headings = ['list_title','list_description']
      uploaded_csv_data = pandas.read_csv(file_path,names=headings, header=None)
      try:
            for c,row_data in uploaded_csv_data.iterrows():
                  task_list=model_task(**row_data,list_userId=user_id)
                  db.session.add(task_list)
                  db.session.commit()
                  current_app.logger.info('Task added to the database')


      except Exception as e:
            current_app.logger.error(e)





