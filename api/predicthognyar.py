from flask import jsonify, request
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import joblib  # Untuk memuat model yang disimpan
import cv2
from skimage.feature import hog
from machine_learning.peprocessing_featureextraction_hog_crop import feature_extraction
from machine_learning.predict_hog_nyar import predict
import numpy as np
# # Membaca gambar
# img = cv2.imread('WhatsApp Image 2024-11-29 at 12.07.41_dc9d9175.jpg')

# # Ekstraksi fitur HOG
# hog_features = preprocess_with_hog(img)

# # Memuat model, scaler, dan PCA
# model = joblib.load('hog_model3.pkl')  # Ganti dengan path model Anda
# scaler = joblib.load('scaler_hog3.pkl')  # Ganti dengan path scaler Anda
# pca = joblib.load('pca_model_hog3.pkl')  # Ganti dengan path PCA Anda

# # Normalisasi fitur
# normalized_features = scaler.transform(hog_features.reshape(1, -1))

# # Reduksi dimensi
# reduced_features = pca.transform(normalized_features)

# # Prediksi menggunakan model
# prediksi = model.predict(reduced_features)

# # Menampilkan confidence score
# if hasattr(model, "predict_proba"):
#     # Jika model mendukung probabilitas
#     probabilities = model.predict_proba(reduced_features)
#     confidence = probabilities.max()  # Confidence untuk kelas yang diprediksi
#     print(f'Hasil prediksi: {prediksi[0]} dengan confidence: {confidence:.2f}')
# elif hasattr(model, "decision_function"):
#     # Jika model mendukung decision_function
#     decision_scores = model.decision_function(reduced_features)
#     confidence = decision_scores.max()  # Skor tertinggi
#     print(f'Hasil prediksi: {prediksi[0]} dengan confidence score: {confidence:.2f}')
# else:
#     print(f'Hasil prediksi: {prediksi[0]} (model tidak mendukung confidence score)')

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
        'confidence':  confidence # Membulatkan confidence ke 2 desimal
    })