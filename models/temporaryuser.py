from datetime import datetime
from config import db

class TemporaryUser(db.Model):
    __tablename__ = 'temporary_users'
    
    # Kolom untuk menyimpan data sementara
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    otp = db.Column(db.String(6), nullable=False)
    otp_expiration = db.Column(db.DateTime, nullable=False)
