from flask_jwt_extended import get_jwt_identity, create_access_token
from flask import jsonify
def verify_token():
    # Mengambil informasi user dari token
    current_user = get_jwt_identity()
    return jsonify({
        "message": "Token is valid",
        "user": current_user
    }), 200

    
def refresh_token():
    current_user = get_jwt_identity()  # Mendapatkan user ID dari refresh token
    new_access_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token), 200  
