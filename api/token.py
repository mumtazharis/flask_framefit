from flask_jwt_extended import get_jwt_identity, create_access_token, jwt_required
from flask import jsonify

# Fungsi untuk memverifikasi access token
@jwt_required()  # Endpoint ini memerlukan access token yang valid
def verify_token():
    current_user = get_jwt_identity()
    return jsonify({
        "message": "Token is valid",
        "user": current_user
    }), 200

# Fungsi untuk merefresh access token
@jwt_required(refresh=True)  # Endpoint ini hanya bisa diakses dengan refresh token
def refresh_token():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token), 200
