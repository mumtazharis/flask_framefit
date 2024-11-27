from sklearn.preprocessing import StandardScaler
import joblib
import numpy as np

# Muat model dan scaler
model = joblib.load('machine_learning/best_svc_model.pkl')
scaler = joblib.load('machine_learning/scaler.pkl')

def predict(fitur):
    # Konversi fitur ke NumPy array
    fitur = np.array(fitur)
    if len(fitur.shape) == 1:
        fitur = np.expand_dims(fitur, axis=0)

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
