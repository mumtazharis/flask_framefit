from flask import jsonify, request
from models import Profile
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from config import db

def get_profile():
    # Mengambil user_id dari token JWT
    user_id = get_jwt_identity()

    # Mencari profil berdasarkan user_id
    profile = Profile.query.filter_by(user_id=user_id).first()

    if profile:
        result = {
            "profile_id": profile.profile_id,
            "user_id": profile.user_id,
            "first_name": profile.first_name,
            "last_name": profile.last_name,
            "email": profile.email,
            "foto_profil": profile.foto_profil
        }
        return jsonify(result), 200
    else:
        return jsonify({"message": "Profile not found"}), 404
    
def edit_profile():
    """Mengedit profil pengguna berdasarkan user_id dari JWT."""
    user_id = get_jwt_identity()  # Mendapatkan user_id dari JWT

    # Mendapatkan profil pengguna
    profile = Profile.query.filter_by(user_id=user_id).first()
    if not profile:
        return jsonify({"error": "Profile not found"}), 404

    # Mengambil data dari request
    data = request.get_json()
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    foto_profil = data.get("foto_profil")  # Opsional

    # Validasi input
    if not email:
        return jsonify({"error": "Email is required."}), 400

    # Update data profil
    if first_name:
        profile.first_name = first_name
    if last_name:
        profile.last_name = last_name
    if email:
        profile.email = email
    if foto_profil:
        profile.foto_profil = foto_profil

    # Simpan perubahan ke database
    db.session.commit()
    return jsonify({"message": "Profile updated successfully."}), 200