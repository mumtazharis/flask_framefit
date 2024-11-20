from config import db
from sqlalchemy import Enum
from datetime import datetime, timedelta
from config import db

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    subscription_status = db.Column(db.String(50), default='free')
    level = db.Column(db.String(50), default='user')