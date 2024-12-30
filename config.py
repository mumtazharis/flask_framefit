# config.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import secrets
from datetime import timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/framefit'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = secrets.token_hex()


app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)  # Masa berlaku access token
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)  # Masa berlaku refresh token

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
