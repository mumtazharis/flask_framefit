import cv2
from mtcnn.mtcnn import MTCNN
import numpy as np
import matplotlib.pyplot as plt
import dlib

def detectFace(image):
    """Mendeteksi wajah menggunakan Haar Cascade dan mengembalikan bounding box wajah terbesar."""
    # Muat Haar Cascade
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Konversi gambar ke skala abu-abu
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Deteksi wajah
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) > 0:
        # Cari wajah dengan area terbesar
        largest_face = max(faces, key=lambda face: face[2] * face[3])  # [x, y, w, h]
        return largest_face
    else:
        return None

def cropFace(image, face, target_size=(224, 224)):
    """Mencrop wajah dari gambar dengan menambahkan buffer dan resize dengan menjaga aspect ratio."""
    if face is not None:
        x, y, w, h = face

        # Menambahkan buffer ke atas dan bawah wajah untuk mencakup seluruh kepala
        buffer_top = int(h * 0.2)  # Tambahkan 20% dari tinggi wajah ke atas
        buffer_bottom = int(h * 0.2)  # Tambahkan 20% dari tinggi wajah ke bawah
        buffer_left = int(w * 0.1)  # Tambahkan 10% dari lebar wajah ke kiri
        buffer_right = int(w * 0.1)  # Tambahkan 10% dari lebar wajah ke kanan

        # Tentukan area crop baru dengan buffer
        y_top = max(0, y - buffer_top)  # Pastikan tidak keluar dari batas gambar
        y_bottom = min(image.shape[0], y + h + buffer_bottom)  # Pastikan tidak keluar dari batas gambar
        x_left = max(0, x - buffer_left)  # Pastikan tidak keluar dari batas gambar
        x_right = min(image.shape[1], x + w + buffer_right)  # Pastikan tidak keluar dari batas gambar

        # Crop gambar dengan area baru
        cropped_face = image[y_top:y_bottom, x_left:x_right]

        # Resize dengan menjaga aspect ratio
        old_h, old_w = cropped_face.shape[:2]
        target_w, target_h = target_size

        # Hitung skala resize
        scale = min(target_w / old_w, target_h / old_h)
        new_w = int(old_w * scale)
        new_h = int(old_h * scale)

        # Resize gambar
        resized_face = cv2.resize(cropped_face, (new_w, new_h), interpolation=cv2.INTER_AREA)

        # Buat canvas hitam untuk padding
        canvas = np.zeros((target_h, target_w, 3), dtype=np.uint8)

        # Hitung offset untuk center padding
        x_offset = (target_w - new_w) // 2
        y_offset = (target_h - new_h) // 2

        # Tempelkan gambar yang di-resize ke canvas
        canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized_face

        return canvas
    else:
        return None

def preprocessing(gambar):
    face = detectFace(gambar)

    if face is not None:
        cropped_face = cropFace(gambar, face)
        rgb_img = cv2.cvtColor(cropped_face, cv2.COLOR_BGR2RGB)
        rgb_img = rgb_img / 255.0
        rgb_img_batch = np.expand_dims(rgb_img, axis=0)
        return rgb_img_batch
    else:
        return None
