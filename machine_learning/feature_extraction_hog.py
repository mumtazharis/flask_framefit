from skimage.feature import hog
import cv2

def extract_hog_features(image, pixels_per_cell=(8, 8), cells_per_block=(2, 2), orientations=9):
    """Ekstraksi fitur HOG dari gambar."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Konversi ke grayscale
    features, hog_image = hog(
        gray, 
        orientations=orientations, 
        pixels_per_cell=pixels_per_cell,
        cells_per_block=cells_per_block, 
        block_norm='L2-Hys', 
        visualize=True,  # Menampilkan gambar HOG
        transform_sqrt=True
    )
    return features, hog_image


def feature_extraction(image):
    features, hog_image = extract_hog_features(image)

    # Tampilkan gambar dengan OpenCV
    cv2.imshow('HOG features',hog_image)
    cv2.waitKey(0)  # Tunggu hingga tombol ditekan
    cv2.destroyAllWindows()  # Tutup jendela

    return features