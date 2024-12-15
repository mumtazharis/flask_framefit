from flask import jsonify, request
import numpy as np
import cv2
from deep_learning.prediction import predict
from deep_learning.preprocessing import preprocessing
import matplotlib.pyplot as plt
import time  # Import modul time

def get_prediction():
    start_time = time.time()  # Catat waktu mulai

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
        predicted_label, confidence = predict(preprocessed_img)
    else:
        # Jika tidak ada wajah terdeteksi, return pesan error
        return jsonify({'error': 'Wajah tidak terdeteksi'}), 400

    end_time = time.time()  # Catat waktu selesai
    processing_time = end_time - start_time  # Hitung waktu pemrosesan

    print(f"Processing Time: {processing_time:.2f} seconds")  # Cetak waktu ke konsol

    return jsonify({
        'predicted_label': predicted_label,
        'confidence': round(float(confidence), 2)  # Membulatkan confidence ke 2 desimal
    })
