from flask import jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from config import db
from models import ContactUs

def contact_admin():
    user_id = get_jwt_identity()
    data = request.get_json()
    new_message = ContactUs(
        user_id=user_id,
        message=data['message']
    )
    db.session.add(new_message)
    db.session.commit()
    return jsonify({"message": "Pesan berhasil terkirim"}), 201
