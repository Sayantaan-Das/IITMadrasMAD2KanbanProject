from flask_security import SQLAlchemyUserDatastore, Security
from application.models import db
from application.models import User, Role



user_datastore = SQLAlchemyUserDatastore(db, User, Role)
sec = Security()


