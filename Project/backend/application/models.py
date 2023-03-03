from application.database import db
from flask_security import UserMixin, RoleMixin
from datetime import datetime, timezone

class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))

class User(db.Model, UserMixin):
    __tablename__='user'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    email=db.Column(db.String(100),unique=True)
    password=db.Column(db.String(255))
    name=db.Column(db.String(100))
    active=db.Column(db.Boolean)
    created=db.Column(db.DateTime,default=datetime.now(timezone.utc))
    monthly_report_format=db.Column(db.String(4),default="pdf")
    receive_reminders_by_webhook=db.Column(db.Boolean, default=False)
    webhook_url=db.Column(db.String())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship(
        'Role', 
        secondary='roles_users', 
        backref=db.backref('users', lazy='dynamic')
    )
    def get_security_payload(self):
            return {
                "name": self.name
            }

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class Card(db.Model):
    __tablename__='cards'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    card_listId = db.Column(db.Integer, db.ForeignKey('lists.id'), nullable=False)
    card_title = db.Column(db.String(80))
    card_content = db.Column(db.String(255))
    card_deadline = db.Column(db.DateTime)
    card_status = db.Column(db.Boolean)
    card_completed_on = db.Column(db.DateTime)
    card_completed_within_deadline = db.Column(db.Boolean)
    card_last_updated = db.Column(db.DateTime)
    def __init__(self,card_listId,card_title,card_content,card_deadline,card_status=False):
        self.card_listId=card_listId
        self.card_title=card_title
        self.card_content=card_content
        self.card_deadline=datetime.strptime(card_deadline,"%Y-%m-%dT%H:%M:%S.%fZ")
        self.card_status= (card_status=="true")
        self.card_completed_on=datetime.now() if (card_status=="true") else None
        self.card_completed_within_deadline=True if ((card_status=="true") and (datetime.strptime(datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),"%Y-%m-%dT%H:%M:%S.%fZ")<self.card_deadline)) else False 
        self.card_last_updated=datetime.now()
    

class TaskList(db.Model):
    __tablename__='lists'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    list_userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    list_title = db.Column(db.String(80))
    list_description = db.Column(db.String(255))
    def __init__(self,list_userId,list_title,list_description):
        self.list_userId=list_userId
        self.list_title=list_title
        self.list_description=list_description