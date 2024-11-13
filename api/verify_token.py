from flask_jwt_extended import get_jwt_identity
from flask import jsonify
def verify_token():
    # Mengambil informasi user dari token
    current_user = get_jwt_identity()
    return jsonify({
        "message": "Token is valid",
        "user": current_user
    }), 200