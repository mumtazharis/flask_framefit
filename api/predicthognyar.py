from flask import jsonify, request
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import joblib  # Untuk memuat model yang disimpan
import cv2
from skimage.feature import hog
from machine_learning.peprocessing_featureextraction_hog_crop import feature_extraction
from machine_learning.predict_hog_nyar import predict
import numpy as np

def get_prediction():
    # Memeriksa apakah ada file gambar yang diunggah
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    image_file = request.files['image']
    in_memory_file = image_file.read()

    # Mengonversi byte data menjadi gambar
    npimg = np.fromstring(in_memory_file, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)



    fitur_hog = feature_extraction(img)
    if fitur_hog is not None:
        label, confidence = predict(fitur_hog)
    else:
        return jsonify({'error': 'Wajah tidak terdeteksi'}), 400


    return jsonify({
        'predicted_label': label,
        'confidence': round(float(confidence), 2) # Membulatkan confidence ke 2 desimal
    })