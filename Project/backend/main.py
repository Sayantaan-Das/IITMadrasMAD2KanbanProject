import logging
from application import create_app
from application.utils.config import LocalDevelopmentConfig
from application.utils.first_request import create_db

dev_app, dev_api, dev_celery, dev_cache=create_app(LocalDevelopmentConfig)

dev_app.before_first_request(create_db)

logging.basicConfig(filename='record.log', level=logging.DEBUG,format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

if (__name__=='__main__'):
    dev_app.run(debug=True,port=8000)

