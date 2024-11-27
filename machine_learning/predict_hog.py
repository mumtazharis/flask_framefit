from sklearn.preprocessing import StandardScaler
import joblib
import numpy as np

# Muat model dan scaler
model = joblib.load('machine_learning/hog_model.pkl')
scaler = joblib.load('machine_learning/scaler_hog.pkl')

def predict(fitur):
    # Pastikan fitur adalah array NumPy dan memiliki dimensi yang sesuai
    fitur = np.array(fitur).reshape(1, -1)  # Memastikan fitur adalah 2D array (1 sampel)

    # Lakukan scaling
    fitur_scaled = scaler.transform(fitur)

    # Prediksi label dan confidence
    label = model.predict(fitur_scaled)[0]  # Ambil elemen pertama (karena hanya satu sampel)
    confidence = model.predict_proba(fitur_scaled)[0]  # Ambil elemen pertama untuk probabilitas

    # Ambil confidence untuk label prediksi
    confidence_for_label = confidence[np.argmax(confidence)]  # Confidence tertinggi

    print("Predicted Label:", label)
    print("Confidence for Label:", confidence_for_label)
    return label, confidence_for_label
