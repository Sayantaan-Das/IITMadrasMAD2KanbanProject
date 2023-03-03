import os

basedir= os.path.abspath(os.path.dirname(__file__))


class Config():
    DEBUG=False
    SQLITE_DB_DIR=None
    SQLALCHEMY_DATABASE_URI=None
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SECURITY_TOKEN_AUTHENTICATION_HEADER="Authentication-Token"
    WTF_CSRF_ENABLED=False
    CELERY_BROKER_URL=""
    CELERY_RESULT_BACKEND=""

class LocalDevelopmentConfig(Config):
    DEBUG=True
    SQLITE_DB_DIR=os.path.join(basedir,"../..","db_folder")
    SQLALCHEMY_DATABASE_URI="sqlite:///"+os.path.join(SQLITE_DB_DIR,"database2.sqlite3")
    SECRET_KEY="Secret"
    SECURITY_PASSWORD_HASH="bcrypt"
    SECURITY_PASSWORD_SALT="Secret"
    SECURITY_REGISTERABLE=False
    SECURITY_SEND_REGISTER_EMAIL=False
    SECURITY_UNAUTHORIZED_VIEW=None
    SECURITY_CHANGEABLE=True
    WTF_CSRF_ENABLED=False
    CELERY_BROKER_URL="redis://localhost:6379/1"
    CELERY_RESULT_BACKEND="redis://localhost:6379/2"
    SMTP_SERVER_HOST="localhost"
    SMTP_SERVER_PORT=1025
    SENDER_ADDRESS="kanbanapplication@project.com"
    SENDER_PASSWORD=""
    MONTHLY_REPORT_TEMPORARY_SAVE_FOLDER=os.path.join(basedir,"../..","static/reports/")
    UPLOAD_ALLOWED_EXTENSIONS=set(['csv'])
    UPLOAD_SAVE_FOLDER=os.path.join(basedir,"../..","static/uploads/")
    TIMEZONE="Asia/Calcutta"
    DOWNLOADABLE_FILES_FOLDER=os.path.join(basedir,"../..","static/downloadable_files/")
    EMAIL_TEMPLATES_PATH=os.path.join(basedir,"../..","Templates/")
    CACHE_TYPE="RedisCache"
    CACHE_REDIS_HOST="localhost"
    CACHE_REDIS_PORT=6379
    SECURITY_EMAIL_VALIDATOR_ARGS = { "check_deliverability" : False }