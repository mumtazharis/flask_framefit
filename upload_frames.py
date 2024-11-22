import os
import logging
from models.kacamata import Kacamata
from config import db
from app import app

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Path folder frames
FRAME_FOLDER = "static/Frames"

# Tambahkan data ke tabel kacamata
with app.app_context():
    for root, dirs, files in os.walk(FRAME_FOLDER):
        for filename in files:
            if filename.endswith(('.png', '.jpg', '.jpeg')):  # Filter file gambar
                folder_name = os.path.basename(root)  # Nama sub-folder
                file_path = os.path.join(root, filename).replace("\\", "/")  # Handle Windows path

                # Tentukan gender berdasarkan nama folder
                if 'Man' in folder_name.lower():
                    gender = 'man'
                elif 'Woman' in folder_name.lower():
                    gender = 'woman'
                else:
                    logging.debug(f"Skipping file {filename} in folder {folder_name}")
                    continue  # Skip files not in 'man' or 'woman' folders

                # Tambahkan ke tabel kacamata
                new_kacamata = Kacamata(
                    model=filename.split('.')[0],  # Nama model dari file
                    jenis=folder_name,             # Nama folder sebagai jenis
                    gender=gender,
                    bentuk=folder_name,            # Asumsikan bentuk sama dengan jenis
                    deskripsi=f"Bingkai tipe {folder_name}",
                    foto=file_path                 # Path relatif gambar
                )
                db.session.add(new_kacamata)
                logging.debug(f"Added {filename} to session")

    try:
        db.session.commit()
        logging.debug("Database commit successful")
    except Exception as e:
        logging.error(f"Error committing to database: {e}")
        db.session.rollback()
