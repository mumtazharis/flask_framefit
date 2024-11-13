from flask import jsonify, request
from config import db
from models import ContactUs

def contact_admin():
    data = request.get_json()
    new_message = ContactUs(
        user_id=data['user_id'],
        message=data['message']
    )
    db.session.add(new_message)
    db.session.commit()
    return jsonify({"message": "Message sent"}), 201
