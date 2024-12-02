import os
from flask import jsonify, request
from config import db
from models import Kacamata


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


def get_rekomendasi():
    if request.is_json:
        data = request.get_json()
        bentuk_wajah = data.get('bentuk_wajah')
    else:
        bentuk_wajah = request.args.get('bentuk_wajah') or request.form.get('bentuk_wajah')

    rekomendasi_map = {
        'Heart': ['Aviator', 'Butterfly', 'CatEye', 'Oval', 'Round', 'Wayfarer'],
        'Oblong': ['Browline', 'Butterfly', 'CatEye', 'Oval', 'Round'],
        'Oval': ['Browline', 'Oval', 'Rectangle', 'Round', 'Sport', 'Wayfarer'],
        'Round': ['Aviator', 'CatEye', 'Geometric', 'Rectangle', 'Sport'],
        'Square': ['Browline', 'Butterfly', 'Oval', 'Round']
    }

    if bentuk_wajah not in rekomendasi_map:
        return jsonify({"error": "Invalid face shape"}), 400

    jenis_kacamata = rekomendasi_map[bentuk_wajah]

    kacamata = Kacamata.query.filter(Kacamata.bentuk.in_(jenis_kacamata)).all()

    result = [
        {
            "kacamata_id": k.kacamata_id,
            "model": k.model,
            "jenis": k.jenis,
            "gender": k.gender,
            "bentuk": k.bentuk,
            "deskripsi": k.deskripsi,
            "foto": f"{request.host_url}{k.foto}"
        }
        for k in kacamata
    ]

    return jsonify(result)

def get_kacamata():
    base_path = os.path.join(os.getcwd(), "static", "Frame")
    photos = []

    for gender in ["male", "female"]:
        gender_path = os.path.join(base_path, gender)
        if os.path.exists(gender_path):
            for category in os.listdir(gender_path):
                category_path = os.path.join(gender_path, category)
                if os.path.isdir(category_path):
                    for filename in os.listdir(category_path):
                        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                            photo_url = f"{request.host_url}static/Frame/{gender}/{category}/{filename}"
                            photos.append({
                                "gender": gender,
                                "category": category,
                                "filename": filename,
                                "url": photo_url
                            })

    return jsonify(photos)
