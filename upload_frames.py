import os
from models.kacamata import Kacamata
from config import db
from app import app

# Path folder frames
FRAME_FOLDER = "static/frames"

# Tambahkan data ke tabel kacamata
with app.app_context():
    for root, dirs, files in os.walk(FRAME_FOLDER):
        for filename in files:
            if filename.endswith(('.png', '.jpg', '.jpeg')):  # Filter file gambar
                folder_name = os.path.basename(root)  # Nama sub-folder
                file_path = os.path.join(root, filename).replace("\\", "/")  # Handle Windows path

                # Tambahkan ke tabel kacamata
                new_kacamata = Kacamata(
                    model=filename.split('.')[0],  # Nama model dari file
                    jenis=folder_name,             # Nama folder sebagai jenis
                    gender="unisex",
                    bentuk=folder_name,            # Asumsikan bentuk sama dengan jenis
                    deskripsi=f"Bingkai tipe {folder_name}",
                    foto=file_path                 # Path relatif gambar
                )
                db.session.add(new_kacamata)

    db.session.commit()
