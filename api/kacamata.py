from flask import jsonify, request
from config import db
from models import Kacamata

def get_kacamata():
    kacamata = Kacamata.query.all()
    result = [{"kacamata_id": k.kacamata_id, "model": k.model, "jenis": k.jenis, "gender": k.gender.value} for k in kacamata]
    return jsonify(result)

def add_kacamata():
    data = request.get_json()
    new_kacamata = Kacamata(
        model=data['model'],
        jenis=data['jenis'],
        gender=data['gender'],
        bentuk=data['bentuk'],
        deskripsi=data.get('deskripsi'),
        foto=data.get('foto')
    )
    db.session.add(new_kacamata)
    db.session.commit()
    return jsonify({"message": "Kacamata added"}), 201
