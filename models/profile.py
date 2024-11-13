from config import db

class Profile(db.Model):
    __tablename__ = 'profiles'
    profile_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(150))
    foto_profil = db.Column(db.String(255), nullable=True)
    user = db.relationship('User', backref=db.backref('profile', uselist=False))
