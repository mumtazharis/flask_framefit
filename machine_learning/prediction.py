from tensorflow.keras.models import load_model
from machine_learning.preprocessing import preprocessing
import cv2
import numpy as np

model = load_model('machine_learning/model_t1.keras')

label_map = {0: 'Heart', 1: 'Oblong', 2: 'Oval', 3: 'Round', 4: 'Square'}

def predict(gambar):

    preprocessed_img = preprocessing(gambar)
    # Mendapatkan prediksi dan probabilitas
    predictions = model.predict(preprocessed_img)
    
    # Menentukan kelas dengan probabilitas tertinggi
    predicted_class = np.argmax(predictions, axis=1)[0]
    predicted_label = label_map[predicted_class]
    
    # Menampilkan confidence (probabilitas dari kelas yang dipilih)
    confidence = predictions[0][predicted_class] * 100  # Mengonversi ke persen
    
    return predicted_label, confidence
