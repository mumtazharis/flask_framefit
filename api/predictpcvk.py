from flask import jsonify, request
from config import db
import numpy as np
import cv2
from machine_learning.preprocessing import preprocessing
from machine_learning.feature_extraction import feature_extraction

def get_prediction():
    # Memeriksa apakah ada file gambar yang diunggah
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    image_file = request.files['image']
    in_memory_file = image_file.read()

    # Mengonversi byte data menjadi gambar
    npimg = np.fromstring(in_memory_file, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)



    preprocessed_img = preprocessing(img)
    if preprocessed_img is not None:
        feature_extraction(preprocessed_img)
    if preprocessed_img is None:
        return jsonify({'error': 'Wajah tidak terdeteksi'}), 400

    return jsonify({
        'predicted_label': 'Wajah berhasil terdeteksi',
        # 'confidence': 'Akurasi ditampilkan disini'  # Membulatkan confidence ke 2 desimal
    })