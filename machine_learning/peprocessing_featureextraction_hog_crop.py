import cv2
import numpy as np
import mediapipe as mp
from skimage.feature import hog

def detectFace(image):
    """Mendeteksi wajah menggunakan Haar Cascade."""
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    if len(faces) > 0:
        largest_face = max(faces, key=lambda face: face[2] * face[3])
        return largest_face
    else:
        return None

def cropFace(image, face, target_size=(224, 224)):
    """Mencrop wajah dan mendeteksi landmark dengan pengurangan background."""
    if face is not None:
        x, y, w, h = face
        buffer_top = int(h * 0.2)
        buffer_bottom = int(h * 0.2)
        buffer_left = int(w * 0.1)
        buffer_right = int(w * 0.1)
        y_top = max(0, y - buffer_top)
        y_bottom = min(image.shape[0], y + h + buffer_bottom)
        x_left = max(0, x - buffer_left)
        x_right = min(image.shape[1], x + w + buffer_right)
        cropped_face = image[y_top:y_bottom, x_left:x_right]
        old_h, old_w = cropped_face.shape[:2]
        target_w, target_h = target_size
        scale = min(target_w / old_w, target_h / old_h)
        new_w = int(old_w * scale)
        new_h = int(old_h * scale)
        resized_face = cv2.resize(cropped_face, (new_w, new_h), interpolation=cv2.INTER_AREA)
        canvas = np.zeros((target_h, target_w, 3), dtype=np.uint8)
        x_offset = (target_w - new_w) // 2
        y_offset = (target_h - new_h) // 2
        canvas[y_offset:y_offset + new_h, x_offset:x_offset + new_w] = resized_face
        # if canvas is not None:
        #     # Tampilkan gambar dengan OpenCV
        #     cv2.imshow('Cropped Image',canvas)
        #     cv2.waitKey(0)  # Tunggu hingga tombol ditekan
        #     cv2.destroyAllWindows()  # Tutup jendela
        # Deteksi landmark menggunakan MediaPipe
        image_rgb = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)

        # Inisialisasi MediaPipe Face Mesh
        mp_face_mesh = mp.solutions.face_mesh
        face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1)

        results = face_mesh.process(image_rgb)

        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark
            
            # Ambil landmark sesuai dengan indeks yang diberikan
            indices = [10, 338, 297, 332, 284, 251, 389, 356, 447, 366, 
                       361, 288, 397, 365, 379, 378, 400, 377, 152, 
                       148, 176, 149, 150, 136, 172, 58, 132, 93, 
                       234, 34, 162, 21, 54, 103, 67, 109]
            selected_landmarks = np.array([[landmarks[i].x, landmarks[i].y] for i in indices]) * [canvas.shape[1], canvas.shape[0]]
            
            mask = np.zeros(canvas.shape[:2], dtype=np.uint8)
            all_points = selected_landmarks.astype(np.int32)
            cv2.fillPoly(mask, [all_points], 255)
            face_only = cv2.bitwise_and(canvas, canvas, mask=mask)
            
            return face_only
    return None

def preprocessing(image):
    
    face = detectFace(image)
    if face is not None:
        cropped_face = cropFace(image, face)
        return cropped_face
    else:
        return None

def standarized_input(image):
    image = preprocessing(image)
    if image is not None:
        return image.astype(np.uint8)
    else:
        return None
    



def extract_hog_features(image, pixels_per_cell=(8, 8), cells_per_block=(2, 2), orientations=9):
    """Ekstraksi fitur HOG dari gambar."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Konversi ke grayscale
    features, hog_image = hog(
        gray, 
        orientations=orientations, 
        pixels_per_cell=pixels_per_cell,
        cells_per_block=cells_per_block, 
        block_norm='L2-Hys', 
        visualize=True,
        transform_sqrt=True
    )
    return features, hog_image

def feature_extraction(image):
    std_img = standarized_input(image)
    if std_img is not None:
        features, hog_image = extract_hog_features(std_img)

        # # Tampilkan gambar dengan OpenCV
        # cv2.imshow('HOG features',hog_image)
        # cv2.waitKey(0)  # Tunggu hingga tombol ditekan
        # cv2.destroyAllWindows()  # Tutup jendela

        return features


