from flask import jsonify
from models import Profile

def get_profile(user_id):
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
        return jsonify(result)
    else:
        return jsonify({"message": "Profile not found"}), 404
