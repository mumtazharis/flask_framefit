from config import db
from sqlalchemy import Enum

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    subscription_status = db.Column(Enum('free', 'premium', name='subscription_types'), nullable=False, default='free')
    level = db.Column(Enum('admin', 'user', name='user_levels'), nullable=False, default='user')
    contact_us = db.relationship('ContactUs', backref='user', lazy=True)
