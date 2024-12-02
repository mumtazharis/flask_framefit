from config import db

class Bookmark(db.Model):
    __tablename__ = 'bookmarks'
    
    bookmark_id = db.Column(db.Integer, primary_key=True)  # Primary Key untuk tabel bookmarks
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)  # Foreign Key ke tabel users
    kacamata_id = db.Column(db.Integer, db.ForeignKey('kacamata.kacamata_id'), nullable=False)  # Foreign Key ke tabel kacamata
    
    # Relasi ke tabel User dan Kacamata
    user = db.relationship('User', backref=db.backref('bookmarks', lazy=True))  # Relasi ke tabel User
    kacamata = db.relationship('Kacamata', backref=db.backref('bookmarks', lazy=True))  # Relasi ke tabel Kacamata
