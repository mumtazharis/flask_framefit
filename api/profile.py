from flask import jsonify
from models import Profile
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

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