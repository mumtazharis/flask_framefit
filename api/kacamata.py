from flask import jsonify, request
from config import db
from models import Kacamata

def get_kacamata():
    kacamata = Kacamata.query.all()
    result = [{"kacamata_id": k.kacamata_id, "model": k.model, "jenis": k.jenis, "gender": k.gender} for k in kacamata]
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

def get_rekomendasi():
    if request.is_json:
        data = request.get_json()
        bentuk_wajah = data.get('bentuk_wajah')
    else:
        bentuk_wajah = request.args.get('bentuk_wajah') or request.form.get('bentuk_wajah')

    # Map bentuk wajah ke jenis kacamata
    rekomendasi_map = {
        'Heart': ['Aviator', 'Butterfly', 'CatEye', 'Oval', 'Round', 'Wayfarer'],
        'Oblong': ['Browline', 'Butterfly', 'CatEye', 'Oval', 'Round'],
        'Oval': ['Browline', 'Oval', 'Rectangle', 'Round', 'Sport', 'Wayfarer'],
        'Round': ['Aviator', 'CatEye', 'Geometric', 'Rectangle', 'Sport'],
        'Square': ['Browline', 'Butterfly', 'Oval', 'Round']
    }

    # Pastikan bentuk_wajah valid
    if bentuk_wajah not in rekomendasi_map:
        return jsonify({"error": "Invalid face shape"}), 400

    # Ambil jenis kacamata yang direkomendasikan untuk bentuk wajah tersebut
    jenis_kacamata = rekomendasi_map[bentuk_wajah]

    # Query database untuk mengambil data kacamata yang sesuai dengan jenis
    kacamata = Kacamata.query.filter(Kacamata.bentuk.in_(jenis_kacamata)).all()

    # Format hasil
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
