from flask import jsonify, request
from config import db
import numpy as np
import cv2
from mtcnn import MTCNN
from deep_learning.prediction import predict
import matplotlib.pyplot as plt

def get_prediction():
    # Memeriksa apakah ada file gambar yang diunggah
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    image_file = request.files['image']
    in_memory_file = image_file.read()

    # Mengonversi byte data menjadi gambar
    npimg = np.fromstring(in_memory_file, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
   

    # Menggunakan MTCNN untuk mendeteksi wajah
    detector = MTCNN()
    detections = detector.detect_faces(img)

    # plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # plt.axis('off')  # Mematikan axis untuk tampilan lebih baik
    # plt.show()  # Tampilkan gambar
    # Jika tidak ada wajah terdeteksi, return pesan error
    if not detections:
        return jsonify({'error': 'Wajah tidak terdeteksi'}), 400

    # Memanggil fungsi prediksi
    predicted_label, confidence = predict(img)

    return jsonify({
        'predicted_label': predicted_label,
        'confidence': round(float(confidence), 2)  # Membulatkan confidence ke 2 desimal
    })
