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
        gender = data.get('gender')
    else:
        bentuk_wajah = request.args.get('bentuk_wajah') or request.form.get('bentuk_wajah')
        gender = request.args.get('gender') or request.form.get('gender')

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

    if gender:
        # Tambahkan filter untuk gender dan Unisex
        kacamata = Kacamata.query.filter(
            Kacamata.bentuk.in_(jenis_kacamata),
            Kacamata.gender.in_([gender, 'unisex'])
        ).all()
    else:
        kacamata = Kacamata.query.filter(
            Kacamata.bentuk.in_(jenis_kacamata)
        ).all()

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
    try:
        # Ambil parameter gender dari request
        gender_filter = request.args.get('gender', '')

        # Jika gender_filter ada, lakukan filter berdasarkan gender
        if gender_filter:
            kacamata = Kacamata.query.filter(Kacamata.gender == gender_filter).all()
        else:
            # Jika tidak ada filter gender, ambil semua kacamata
            kacamata = Kacamata.query.all()

        # Bangun respons JSON dengan memastikan path foto valid
        result = [
            {
                "kacamata_id": k.kacamata_id,
                "model": k.model,
                "jenis": k.jenis,
                "gender": k.gender,
                "bentuk": k.bentuk,
                "deskripsi": k.deskripsi,
                # Pastikan path foto dilengkapi URL server
                "foto": f"{request.host_url.rstrip('/')}/{k.foto}" 
            }
            for k in kacamata
        ]

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": f"Gagal memuat data kacamata: {str(e)}"}), 500

