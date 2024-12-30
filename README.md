**Kelompok**: 2  
**Anggota Kelompok**:  
- Ahmad Mumtaz Haris (2241720136)
- Nanda Putra Khamdani (2241720180)
- Sukma Bagus Wahasdwika (2241720223)
- Triyana Dewi Fatmawati (2241720206)
---
# Backend FrameFit

Selamat datang di **Backend FrameFit**! Proyek ini merupakan bagian backend dari aplikasi **FrameFit**, yang dirancang untuk merekomendasikan kacamata berdasarkan bentuk wajah pengguna.

## 🚀 Langkah-langkah Instalasi dan Menjalankan Proyek

Ikuti langkah-langkah di bawah ini untuk menjalankan proyek backend secara lokal:

### 1️⃣ Clone Repository
Clone repository ini ke komputer Anda:
```bash
git clone <repository-url>
cd <nama-folder-repository>
```

### 2️⃣ Buat Virtual Environment
Buat lingkungan virtual untuk mengelola dependensi:
```bash
virtualenv myenv
```

### 3️⃣ Aktifkan Virtual Environment
Aktifkan virtual environment yang telah dibuat:
- **Windows**:
  ```bash
  myenv\Scripts\activate
  ```
- **Linux/MacOS**:
  ```bash
  source myenv/bin/activate
  ```

### 4️⃣ Install Dependensi
Install semua dependensi yang dibutuhkan dari file `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 5️⃣ Konfigurasi Database
- Sesuaikan konfigurasi database anda pada file config.py, kemudian hapus folder migrations
- Inisialisasi dan migrasi database menggunakan Flask-Migrate:
  ```bash
  flask db init
  flask db migrate
  flask db upgrade
  ```
(opsional): Jalankan file `upload_frames.py` untuk memasukkan data kacamata yang sudah ada kedalam database

### 6️⃣ Jalankan Server
Jalankan server backend:
```bash
python app.py
```

---

## 📁 File Tambahan

Beberapa file diperlukan untuk melakukan prediksi dengan machine learning atau deep learning:

- **Dlib Shape Predictor**:  
  [Unduh Dlib Shape Predictor](https://github.com/codeniko/shape_predictor_81_face_landmarks/blob/master/shape_predictor_81_face_landmarks.dat)

- **Model HOG**:  
  [Unduh Model HOG](https://drive.google.com/file/d/1OYDqyBXQxPN-0lem71x4B3mM02WbKadT/view?usp=sharing)

- **Model Deep Learning**:  
  [Unduh Model Deep Learning](https://drive.google.com/file/d/17HwelfTi2Qy6On6I_fwIUXOOcJxOiLif/view?usp=sharing)

- **Model HOG Baru**:\
  [Unduh Model HOG Baru](https://drive.google.com/file/d/1RwzhQ2vUsiA_pVDYJRgs4zM1cpLU5tzw/view?usp=sharing)

Setelah mengunduh file di atas, letakkan file **Dlib Shape Predictor** dan **Model HOG** ke dalam folder `machine_learning` dan file **Model Deep Learning** ke dalam folder `deep_learning`. Untuk Model HOG Baru, ekstrak terlebih dahulu kemudian pindahkan isi file ke dalam foler `machine-learning`

---

## 🔧 Menyesuaikan Prediksi

Anda dapat menyesuaikan jenis prediksi yang digunakan dengan mengubah file `api/api.py`:

- **Machine Learning dengan Landmark**:
  ```python
  from api.predictpcvk import get_prediction
  ```

- **Machine Learning dengan HOG lama**:
  ```python
  from api.predicthog import get_prediction
  ```

- **Deep Learning**:
  ```python
  from api.predict import get_prediction
  ```

- **Machine Learning dengan HOG Baru**:
  ```python
  from api.predicthognyar import get_prediction
  ```