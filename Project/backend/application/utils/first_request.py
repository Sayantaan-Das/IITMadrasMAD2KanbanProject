from application.database import db

def create_db():
    db.create_all()