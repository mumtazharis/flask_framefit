import dlib
import cv2
import numpy as np
import matplotlib.pyplot as plt



def detectLandmarks(image):
    # Path ke predictor
    predictor_path = 'machine_learning/shape_predictor_81_face_landmarks.dat'

    # Inisialisasi detektor dan predictor
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(predictor_path)

    # Deteksi wajah pada gambar
    dets = detector(image, 1)
    for d in dets:
        # Dapatkan landmark wajah
        shape = predictor(image, d)
        landmarks = np.matrix([[p.x, p.y] for p in shape.parts()])
        
        # Tampilkan titik landmark di wajah dan tambahkan angka
        for num in range(shape.num_parts):
            x = shape.parts()[num].x
            y = shape.parts()[num].y
            # Gambar titik
            cv2.circle(image, (x, y), 3, (0, 255, 0), -1)
            # Tampilkan angka di atas titik
            cv2.putText(image, str(num), (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1, cv2.LINE_AA)

    return landmarks


def lineLandmarks(image, landmarks):
    # Gambar garis untuk jarak D1 hingga D7
    # D1: Landmark 2 dan 14
    cv2.line(image, (landmarks[2, 0], landmarks[2, 1]), (landmarks[14, 0], landmarks[14, 1]), (255, 0, 0), 1)
    # D2: Landmark 76 dan 79
    cv2.line(image, (landmarks[76, 0], landmarks[76, 1]), (landmarks[79, 0], landmarks[79, 1]), (255, 0, 0), 1)
    # D3: Landmark 8 dan 71
    cv2.line(image, (landmarks[8, 0], landmarks[8, 1]), (landmarks[71, 0], landmarks[71, 1]), (255, 0, 0), 1)
    # D4: Landmark 8 dan 12
    cv2.line(image, (landmarks[8, 0], landmarks[8, 1]), (landmarks[12, 0], landmarks[12, 1]), (255, 0, 0), 1)
    # D5: Landmark 4 dan 12
    cv2.line(image, (landmarks[4, 0], landmarks[4, 1]), (landmarks[12, 0], landmarks[12, 1]), (255, 0, 0), 1)
    # D6: Landmark 6 dan 10
    cv2.line(image, (landmarks[6, 0], landmarks[6, 1]), (landmarks[10, 0], landmarks[10, 1]), (255, 0, 0), 1)
    # D7: Landmark 7 dan 9
    cv2.line(image, (landmarks[7, 0], landmarks[7, 1]), (landmarks[9, 0], landmarks[9, 1]), (255, 0, 0), 1)

    return image

# Fungsi untuk menghitung panjang garis
def line_length(point1, point2):
    return np.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

def hitungsudut(p1, p2, p3):
    # Buat vektor dari titik-titik
    vec1 = np.array([p2[0] - p1[0], p2[1] - p1[1]])
    vec2 = np.array([p3[0] - p1[0], p3[1] - p1[1]])

    # Hitung dot product dan magnitudo kedua vektor
    dot_product = np.dot(vec1, vec2)
    magnitude1 = np.linalg.norm(vec1)
    magnitude2 = np.linalg.norm(vec2)

    # Hitung sudut dalam radian dan konversikan ke derajat
    cos_angle = dot_product / (magnitude1 * magnitude2)
    angle = np.arccos(cos_angle) * (180.0 / np.pi)
    return angle


def landmarkFeature(landmarks):
    # Garis dan panjang masing-masing
    D1_length = line_length((landmarks[2, 0], landmarks[2, 1]), (landmarks[14, 0], landmarks[14, 1]))
    D2_length = line_length((landmarks[76, 0], landmarks[76, 1]), (landmarks[79, 0], landmarks[79, 1]))
    D3_length = line_length((landmarks[8, 0], landmarks[8, 1]), (landmarks[71, 0], landmarks[71, 1]))
    D4_length = line_length((landmarks[8, 0], landmarks[8, 1]), (landmarks[12, 0], landmarks[12, 1]))
    D5_length = line_length((landmarks[4, 0], landmarks[4, 1]), (landmarks[12, 0], landmarks[12, 1]))
    D6_length = line_length((landmarks[6, 0], landmarks[6, 1]), (landmarks[10, 0], landmarks[10, 1]))
    D7_length = line_length((landmarks[7, 0], landmarks[7, 1]), (landmarks[9, 0], landmarks[9, 1]))

    R1 = D2_length / D1_length
    R2 = D1_length / D3_length
    R3 = D2_length / D3_length
    R4 = D1_length / D5_length
    R5 = D6_length / D5_length
    R6 = D4_length / D6_length
    R7 = D6_length / D1_length
    R8 = D5_length / D2_length
    R9 = D4_length / D5_length
    R10 = D7_length / D6_length

    angle1 = hitungsudut((landmarks[8, 0], landmarks[8, 1]),(landmarks[71, 0], landmarks[71, 1]), (landmarks[10, 0], landmarks[10, 1]))
    #Sudut 2
    angle2 = hitungsudut((landmarks[8, 0], landmarks[8, 1]),(landmarks[71, 0], landmarks[71, 1]), (landmarks[12, 0], landmarks[12, 1]))
    #Sudut 3
    angle3 = hitungsudut((landmarks[14, 0], landmarks[14, 1]),(landmarks[2, 0], landmarks[2, 1]), (landmarks[12, 0], landmarks[12, 1]))

    return [D1_length, D2_length, D3_length, D4_length, D5_length, D6_length, D7_length, R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, angle1, angle2, angle3]

def feature_extraction(image):
    landmark = detectLandmarks(image)
    line_landmarks = lineLandmarks(image.copy(), landmark)
    landmark_features = landmarkFeature(landmark)

    # Tampilkan gambar dengan OpenCV
    cv2.imshow('Landmarks',line_landmarks)
    cv2.waitKey(0)  # Tunggu hingga tombol ditekan
    cv2.destroyAllWindows()  # Tutup jendela

    for i, feature in enumerate(landmark_features, 1):
        print(f"Feature {i}: {feature:.2f}")