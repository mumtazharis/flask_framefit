from config import db
from sqlalchemy import Enum

class Kacamata(db.Model):
    __tablename__ = 'kacamata'
    kacamata_id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(100), nullable=False)
    jenis = db.Column(db.String(50), nullable=False)
    gender = db.Column(Enum('male', 'female', 'unisex', name='gender_types'), nullable=False)
    bentuk = db.Column(db.String(50), nullable=False)
    deskripsi = db.Column(db.Text, nullable=True)
    foto = db.Column(db.String(255), nullable=True)
