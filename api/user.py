from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from config import db
from models import User

# Setup JWT
jwt = JWTManager()

# Route untuk login
def login_user():
    data = request.get_json()

    # Validasi input
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"message": "Username dan password diperlukan"}), 400

    # Mencari pengguna berdasarkan username
    user = User.query.filter_by(username=data['username']).first()

    if user and check_password_hash(user.password, data['password']):
        # Membuat token JWT jika login berhasil
        access_token = create_access_token(identity=user.user_id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"message": "Username atau password salah"}), 401

# Route untuk mengambil daftar pengguna
def get_users():
    users = User.query.all()
    result = [{"user_id": user.user_id, "username": user.username, "level": user.level} for user in users]
    return jsonify(result)

# Route untuk menambah pengguna baru
def add_user():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"message": "Username dan password diperlukan"}), 400

    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_user = User(
        username=data['username'],
        password=hashed_password,
        subscription_status=data.get('subscription_status', 'free'),
        level=data.get('level', 'user')
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User added"}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": f"Terjadi kesalahan: {str(e)}"}), 500
