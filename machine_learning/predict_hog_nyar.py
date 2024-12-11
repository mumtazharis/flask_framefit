from sklearn.preprocessing import StandardScaler
import joblib
import numpy as np
# Memuat model, scaler, dan PCA
model = joblib.load('machine_learning/hog_model3.pkl')  # Ganti dengan path model Anda
scaler = joblib.load('machine_learning/scaler_hog3.pkl')  # Ganti dengan path scaler Anda
pca = joblib.load('machine_learning/pca_model_hog3.pkl')  # Ganti dengan path PCA Anda


def predict(fitur):
    # Pastikan fitur adalah array NumPy dan memiliki dimensi yang sesuai
    fitur = np.array(fitur).reshape(1, -1)  # Memastikan fitur adalah 2D array (1 sampel)

    # Lakukan scaling
    fitur_scaled = scaler.transform(fitur)
    reduced_features = pca.transform(fitur_scaled)
    # Prediksi label dan confidence
    label = model.predict(reduced_features)[0]  # Ambil elemen pertama (karena hanya satu sampel)
    confidence = model.predict_proba(reduced_features)[0]  # Ambil elemen pertama untuk probabilitas

    # Ambil confidence untuk label prediksi
    confidence_for_label = confidence[np.argmax(confidence)]  # Confidence tertinggi

    print("Predicted Label:", label)
    print("Confidence for Label:", confidence_for_label)
    return label, confidence_for_label
