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
    # Daftar pasangan titik untuk garis umum
    lines = [
        (1, 15), (8, 71), (75, 79), (2, 14), (3, 13), (4, 12),
        (5, 11), (6, 10), (7, 9), (8, 9), (8, 7),
        (8, 10), (8, 6), (8, 11), (8, 5), (8, 12), (8, 4),
        (8, 13), (8, 3), (8, 14), (8, 2)
    ]

    # Gambar garis umum
    for start, end in lines:
        cv2.line(
            image,
            (landmarks[start, 0], landmarks[start, 1]),
            (landmarks[end, 0], landmarks[end, 1]),
            (255, 0, 0),  # Warna biru dalam format BGR
            1             # Ketebalan garis
        )
    
    # Garis rahang kiri
    rahang_kiri_points = [8, 9, 10, 11, 12, 13, 14]
    for i in range(len(rahang_kiri_points) - 1):
        cv2.line(
            image,
            (landmarks[rahang_kiri_points[i], 0], landmarks[rahang_kiri_points[i], 1]),
            (landmarks[rahang_kiri_points[i + 1], 0], landmarks[rahang_kiri_points[i + 1], 1]),
            (0, 255, 0),  # Warna hijau
            1
        )

    # Garis rahang kanan
    rahang_kanan_points = [8, 7, 6, 5, 4, 3, 2]
    for i in range(len(rahang_kanan_points) - 1):
        cv2.line(
            image,
            (landmarks[rahang_kanan_points[i], 0], landmarks[rahang_kanan_points[i], 1]),
            (landmarks[rahang_kanan_points[i + 1], 0], landmarks[rahang_kanan_points[i + 1], 1]),
            (0, 255, 0),  # Warna hijau
            1
        )

    # Garis atas kiri
    atas_kiri_points = [16, 78, 74, 79, 73, 72]
    for i in range(len(atas_kiri_points) - 1):
        cv2.line(
            image,
            (landmarks[atas_kiri_points[i], 0], landmarks[atas_kiri_points[i], 1]),
            (landmarks[atas_kiri_points[i + 1], 0], landmarks[atas_kiri_points[i + 1], 1]),
            (0, 0, 255),  # Warna merah
            1
        )

    # Garis atas kanan
    atas_kanan_points = [0, 77, 75, 76, 68, 69]
    for i in range(len(atas_kanan_points) - 1):
        cv2.line(
            image,
            (landmarks[atas_kanan_points[i], 0], landmarks[atas_kanan_points[i], 1]),
            (landmarks[atas_kanan_points[i + 1], 0], landmarks[atas_kanan_points[i + 1], 1]),
            (0, 0, 255),  # Warna merah
            1
        )

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
    rahang_kiri = line_length((landmarks[8, 0], landmarks[8, 1]), (landmarks[9, 0], landmarks[9, 1])) + line_length((landmarks[9, 0], landmarks[9, 1]), (landmarks[10, 0], landmarks[10, 1])) + line_length((landmarks[10, 0], landmarks[10, 1]), (landmarks[11, 0], landmarks[11, 1])) + line_length((landmarks[11, 0], landmarks[11, 1]), (landmarks[12, 0], landmarks[12, 1])) + line_length((landmarks[12, 0], landmarks[12, 1]), (landmarks[13, 0], landmarks[13, 1])) + line_length((landmarks[13, 0], landmarks[13, 1]), (landmarks[14, 0], landmarks[14, 1]))
    rahang_kanan = line_length((landmarks[8, 0], landmarks[8, 1]), (landmarks[7, 0], landmarks[7, 1])) + line_length((landmarks[7, 0], landmarks[7, 1]), (landmarks[6, 0], landmarks[6, 1])) + line_length((landmarks[6, 0], landmarks[6, 1]), (landmarks[5, 0], landmarks[5, 1])) + line_length((landmarks[5, 0], landmarks[5, 1]), (landmarks[4, 0], landmarks[4, 1])) + line_length((landmarks[4, 0], landmarks[4, 1]), (landmarks[3, 0], landmarks[3, 1])) + line_length((landmarks[3, 0], landmarks[3, 1]), (landmarks[2, 0], landmarks[2, 1]))
    rahang = (rahang_kanan + rahang_kiri)/2
    atas_kiri = line_length((landmarks[16, 0], landmarks[16, 1]), (landmarks[78, 0], landmarks[78, 1])) + line_length((landmarks[78, 0], landmarks[78, 1]), (landmarks[74, 0], landmarks[74, 1])) + line_length((landmarks[74, 0], landmarks[74, 1]), (landmarks[79, 0], landmarks[79, 1])) + line_length((landmarks[79, 0], landmarks[79, 1]), (landmarks[73, 0], landmarks[73, 1])) + line_length((landmarks[73, 0], landmarks[73, 1]), (landmarks[72, 0], landmarks[72, 1]))

    atas_kanan = line_length((landmarks[0, 0], landmarks[0, 1]), (landmarks[77, 0], landmarks[77, 1])) + line_length((landmarks[77, 0], landmarks[77, 1]), (landmarks[75, 0], landmarks[75, 1])) + line_length((landmarks[75, 0], landmarks[75, 1]), (landmarks[76, 0], landmarks[76, 1])) + line_length((landmarks[76, 0], landmarks[76, 1]), (landmarks[68, 0], landmarks[68, 1])) + line_length((landmarks[68, 0], landmarks[68, 1]), (landmarks[69, 0], landmarks[69, 1]))
    atas = (atas_kanan + atas_kiri)/2
    # Hitung panjang 
    D0_length = line_length((landmarks[1, 0], landmarks[1, 1]), (landmarks[15, 0], landmarks[15, 1]))
    D1_length = line_length((landmarks[8, 0], landmarks[8, 1]), (landmarks[71, 0], landmarks[71, 1]))
    D2_length = line_length((landmarks[75, 0], landmarks[75, 1]), (landmarks[79, 0], landmarks[79, 1]))
    D3_length = line_length((landmarks[2, 0], landmarks[2, 1]), (landmarks[14, 0], landmarks[14, 1]))
    D4_length = line_length((landmarks[3, 0], landmarks[3, 1]), (landmarks[13, 0], landmarks[13, 1]))
    D5_length = line_length((landmarks[4, 0], landmarks[4, 1]), (landmarks[12, 0], landmarks[12, 1]))
    D6_length = line_length((landmarks[5, 0], landmarks[5, 1]), (landmarks[11, 0], landmarks[11, 1]))
    D7_length = line_length((landmarks[6, 0], landmarks[6, 1]), (landmarks[10, 0], landmarks[10, 1]))
    D8_length = line_length((landmarks[7, 0], landmarks[7, 1]), (landmarks[9, 0], landmarks[9, 1]))

    D9_length = line_length((landmarks[8, 0], landmarks[8, 1]), (landmarks[9, 0], landmarks[9, 1]))
    D91_length = line_length((landmarks[8, 0], landmarks[8, 1]), (landmarks[7, 0], landmarks[7, 1]))
    
    D10_length = line_length((landmarks[8, 0], landmarks[8, 1]), (landmarks[10, 0], landmarks[10, 1]))
    D101_length = line_length((landmarks[8, 0], landmarks[8, 1]), (landmarks[6, 0], landmarks[6, 1]))
    
    D11_length = line_length((landmarks[8, 0], landmarks[8, 1]), (landmarks[11, 0], landmarks[11, 1]))
    D111_length = line_length((landmarks[8, 0], landmarks[8, 1]), (landmarks[5, 0], landmarks[5, 1]))
    
    D12_length = line_length((landmarks[8, 0], landmarks[8, 1]), (landmarks[12, 0], landmarks[12, 1]))
    D121_length = line_length((landmarks[8, 0], landmarks[8, 1]), (landmarks[4, 0], landmarks[4, 1]))
    
    D13_length = line_length((landmarks[8, 0], landmarks[8, 1]), (landmarks[13, 0], landmarks[13, 1]))
    D131_length = line_length((landmarks[8, 0], landmarks[8, 1]), (landmarks[3, 0], landmarks[3, 1]))
    
    D14_length = line_length((landmarks[8, 0], landmarks[8, 1]), (landmarks[14, 0], landmarks[14, 1]))
    D141_length = line_length((landmarks[8, 0], landmarks[8, 1]), (landmarks[2, 0], landmarks[2, 1]))
    

    Sum_D = D1_length + D2_length + D3_length + D4_length + D5_length + D6_length + D7_length + D8_length + (D9_length + D91_length)/2 
    + (D10_length + D101_length)/2 + (D11_length + D111_length)/2 + (D12_length + D121_length)/2 + (D13_length + D131_length)/2 + (D14_length + D141_length)/2

    D0 = D0_length / Sum_D
    D1 = D1_length / Sum_D
    D2 = D2_length / Sum_D
    D3 = D3_length / Sum_D
    D4 = D4_length / Sum_D
    D5 = D5_length / Sum_D
    D6 = D6_length / Sum_D
    D7 = D7_length / Sum_D
    D8 = D8_length / Sum_D
    D9 = ((D9_length / Sum_D) + (D91_length / Sum_D)) / 2
    D10 = ((D10_length / Sum_D) + (D101_length / Sum_D)) / 2
    D11 = ((D11_length / Sum_D) + (D111_length / Sum_D)) / 2
    D12 = ((D12_length / Sum_D) + (D121_length / Sum_D)) / 2
    D13 = ((D13_length / Sum_D) + (D131_length / Sum_D)) / 2
    D14 = ((D14_length / Sum_D) + (D141_length / Sum_D)) / 2

    # Hitung rasio
    R1 = D0 / D3
    R2 = D0 / D4
    R3 = D0 / D5
    R4 = D0 / D6
    R5 = D0 / D7
    R6 = D0 / D8
    R7 = D6 / D1
    R8 = D5 / D2
    R9 = D4 / D5
    R10 = D7 / D6

    # Hitung sudut
    angle1a = hitungsudut((landmarks[8, 0], landmarks[8, 1]), (landmarks[71, 0], landmarks[71, 1]), (landmarks[10, 0], landmarks[10, 1]))
    angle1b = hitungsudut((landmarks[8, 0], landmarks[8, 1]), (landmarks[71, 0], landmarks[71, 1]), (landmarks[6, 0], landmarks[6, 1]))
    angle1 = (angle1a + angle1b)/2
    angle2a = hitungsudut((landmarks[8, 0], landmarks[8, 1]), (landmarks[71, 0], landmarks[71, 1]), (landmarks[12, 0], landmarks[12, 1]))
    angle2b = hitungsudut((landmarks[8, 0], landmarks[8, 1]), (landmarks[71, 0], landmarks[71, 1]), (landmarks[4, 0], landmarks[4, 1]))
    angle2 = (angle2a+angle2b)/2
    angle3a = hitungsudut((landmarks[14, 0], landmarks[14, 1]), (landmarks[2, 0], landmarks[2, 1]), (landmarks[12, 0], landmarks[12, 1]))
    angle3b = hitungsudut((landmarks[2, 0], landmarks[2, 1]), (landmarks[14, 0], landmarks[14, 1]), (landmarks[4, 0], landmarks[4, 1]))
    angle3 = (angle3a+angle3b)/2
    angle4a = hitungsudut((landmarks[9, 0], landmarks[9, 1]), (landmarks[8, 0], landmarks[8, 1]), (landmarks[10, 0], landmarks[10, 1]))
    angle4b = hitungsudut((landmarks[7, 0], landmarks[7, 1]), (landmarks[8, 0], landmarks[8, 1]), (landmarks[6, 0], landmarks[6, 1]))
    angle4 = (angle4a+angle4b)/2
    angle5a = hitungsudut((landmarks[11, 0], landmarks[11, 1]), (landmarks[10, 0], landmarks[10, 1]), (landmarks[12, 0], landmarks[12, 1]))
    angle5b = hitungsudut((landmarks[5, 0], landmarks[5, 1]), (landmarks[6, 0], landmarks[6, 1]), (landmarks[4, 0], landmarks[4, 1]))
    angle5 = (angle5a+angle5b)/2
    angle6a = hitungsudut((landmarks[13, 0], landmarks[13, 1]), (landmarks[12, 0], landmarks[12, 1]), (landmarks[14, 0], landmarks[14, 1]))
    angle6b = hitungsudut((landmarks[3, 0], landmarks[3, 1]), (landmarks[4, 0], landmarks[4, 1]), (landmarks[2, 0], landmarks[2, 1]))
    angle6 = (angle6a+angle6b)/2
    angle7 = hitungsudut((landmarks[8, 0], landmarks[8, 1]), (landmarks[7, 0], landmarks[7, 1]), (landmarks[9, 0], landmarks[9, 1]))


    return [D1, D2, D3, D4, D5, D6, D7, D8, D9, D10, D11, D12, D13, D14, R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, angle1, angle2, angle3, angle4, angle5, angle6, angle7, rahang, atas]

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

    return landmark_features