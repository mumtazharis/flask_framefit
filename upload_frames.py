import os
from models.kacamata import Kacamata
from config import db
from app import app

# Path folder frames
FRAME_FOLDER = "static/Frame"

# Fungsi untuk mendeteksi gender berdasarkan path
def detect_gender_from_path(path):
    if "man" in path.lower():
        return "male"
    elif "woman" in path.lower():
        return "female"
    return "unisex"

# Tambahkan data ke tabel kacamata
with app.app_context():
    # Iterasi folder utama
    for root, dirs, files in os.walk(FRAME_FOLDER):
        for filename in files:
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):  # Filter file gambar
                # Dapatkan path file
                file_path = os.path.join(root, filename).replace("\\", "/")
                folder_path = os.path.normpath(root)  # Path folder saat ini
                folder_parts = folder_path.split(os.sep)  # Pisahkan path menjadi bagian-bagian

                # Tentukan gender dari folder `man` atau `woman`
                gender = "unisex"
                if len(folder_parts) >= 3:  # Pastikan struktur folder cukup panjang
                    if "man" in folder_parts:
                        gender = "male"
                    elif "woman" in folder_parts:
                        gender = "female"

                # Tentukan jenis dari folder terakhir
                jenis = folder_parts[-1]

                # Debugging tambahan
                print(f"Processing file: {file_path}")
                print(f"Detected gender: {gender}, Jenis: {jenis}")

                # Tambahkan data ke tabel kacamata
                new_kacamata = Kacamata(
                    model=filename.split('.')[0],  # Nama model dari file
                    jenis=jenis,                   # Nama folder terakhir sebagai jenis
                    gender=gender,
                    bentuk=jenis,                  # Asumsikan bentuk sama dengan jenis
                    deskripsi=f"Bingkai tipe {jenis}",
                    foto=file_path                 # Path relatif gambar
                )
                db.session.add(new_kacamata)

    # Simpan semua perubahan ke database
    db.session.commit()
