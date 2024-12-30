from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, get_jwt_identity
from config import db
from models import User, TemporaryUser, Profile
# from utils import send_email
from datetime import datetime, timedelta
import pyotp
import smtplib
from email.mime.text import MIMEText

# Setup JWT
jwt = JWTManager()

# Route untuk login
def login_user():
    data = request.get_json()

    # Validasi input
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"message": "Username dan password diperlukan"}), 400

    # Mencari pengguna berdasarkan username
    user = User.query.filter_by(username=data['username']).first()

    if user and check_password_hash(user.password, data['password']):
        # Membuat access dan refresh token
        access_token = create_access_token(identity=user.user_id)
        refresh_token = create_refresh_token(identity=user.user_id)

        return jsonify(access_token=access_token, refresh_token=refresh_token), 200
    else:
        return jsonify({"message": "Username atau password salah"}), 401
    


def register():
    data = request.get_json()
    username = data.get('email')
    otp = data.get('otp')
    password = data.get('password')
    first_name = data.get('first_name', "")  # Ambil first_name dari request
    last_name = data.get('last_name', "")    # Ambil last_name dari request

    # Validasi input
    if not username or not otp or not password or not first_name or not last_name:
        return jsonify({"message": "Semua data diperlukan"}), 400

    # Cari pengguna sementara berdasarkan email
    temp_user = TemporaryUser.query.filter_by(username=username).first()
    if not temp_user:
        return jsonify({"message": "Email tidak ditemukan"}), 404

    # Verifikasi OTP
    if temp_user.otp != otp or temp_user.otp_expiration < datetime.now():
        return jsonify({"message": "OTP salah atau sudah kadaluarsa"}), 400

    try:
        # Simpan pengguna permanen ke tabel User
        new_user = User(username=username, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()  # Commit untuk mendapatkan user_id

        # Buat entitas Profile berdasarkan user
        new_profile = Profile(
            user_id=new_user.user_id,  # Ambil user_id dari tabel User
            email=new_user.username,
            first_name=first_name,  # Diambil dari request
            last_name=last_name,    # Diambil dari request
        )
        db.session.add(new_profile)
        db.session.delete(temp_user)  # Hapus pengguna sementara setelah registrasi
        db.session.commit()

        return jsonify({"message": "Registrasi berhasil"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Terjadi kesalahan: {str(e)}"}), 500

def send_email(to_email, otp):
    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "jti.framefit@gmail.com"
        sender_password = "kxoj ydqs prhi pizf"

        msg = MIMEText(f"Kode OTP Anda adalah: {otp}")
        msg['Subject'] = "Kode OTP"
        msg['From'] = sender_email
        msg['To'] = to_email

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
    except Exception as e:
        print(f"Error saat mengirim email: {e}")


def send_otp():
    data = request.get_json()
    username = data.get('email')

    # Validasi email
    if not username:
        return jsonify({"message": "Email diperlukan"}), 400

    # Periksa apakah email sudah terdaftar di tabel User (pengguna permanen)
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"message": "Email sudah digunakan"}), 400

    # Generate OTP
    otp = pyotp.random_base32()[:6]  # 6 digit OTP
    otp_expiration = datetime.now() + timedelta(minutes=5)  # OTP berlaku 5 menit

    # Periksa apakah username sudah ada di tabel TemporaryUser
    temp_user = TemporaryUser.query.filter_by(username=username).first()
    if temp_user:
        # Jika sudah ada, perbarui OTP dan tanggal kedaluwarsa
        temp_user.otp = otp
        temp_user.otp_expiration = otp_expiration
    else:
        # Jika belum ada, tambahkan pengguna sementara baru
        temp_user = TemporaryUser(username=username, otp=otp, otp_expiration=otp_expiration)
        db.session.add(temp_user)

    # Simpan perubahan ke database
    db.session.commit()

    # Kirim OTP melalui email
    send_email(username, otp)

    return jsonify({"message": "OTP telah dikirim ke email"}), 200

def ubah_password():
    data = request.get_json()
    user_id = get_jwt_identity()  # Ambil user_id dari token JWT

    # Validasi input
    password_lama = data.get('password_lama')
    password_baru = data.get('password_baru')
    konfirmasi_password = data.get('konfirmasi_password')

    if not password_lama or not password_baru or not konfirmasi_password:
        return jsonify({"message": "Semua data diperlukan"}), 400

    if password_baru != konfirmasi_password:
        return jsonify({"message": "Password baru dan konfirmasi tidak cocok"}), 400

    # Cari pengguna berdasarkan user_id
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        return jsonify({"message": "Pengguna tidak ditemukan"}), 404

    # Verifikasi password lama
    if not check_password_hash(user.password, password_lama):
        return jsonify({"message": "Password lama salah"}), 401

    # Update password
    try:
        user.password = generate_password_hash(password_baru)
        db.session.commit()
        return jsonify({"message": "Password berhasil diubah"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Terjadi kesalahan: {str(e)}"}), 500
    
def send_otp_sandi():
    data = request.get_json()
    username = data.get('email')

    # Validasi email
    if not username:
        return jsonify({"message": "Email diperlukan"}), 400

    # Periksa apakah email sudah terdaftar di tabel User (pengguna permanen)
    existing_user = User.query.filter_by(username=username).first()
    if not existing_user:
        return jsonify({"message": "Email tidak terdaftar"}), 404

    # Generate OTP
    otp = pyotp.random_base32()[:6]  # 6 digit OTP
    otp_expiration = datetime.now() + timedelta(minutes=5)  # OTP berlaku 5 menit

    # Periksa apakah username sudah ada di tabel TemporaryUser
    temp_user = TemporaryUser.query.filter_by(username=username).first()
    if temp_user:
        # Jika sudah ada, perbarui OTP dan tanggal kedaluwarsa
        temp_user.otp = otp
        temp_user.otp_expiration = otp_expiration
    else:
        # Jika belum ada, tambahkan pengguna sementara baru
        temp_user = TemporaryUser(username=username, otp=otp, otp_expiration=otp_expiration)
        db.session.add(temp_user)

    # Simpan perubahan ke database
    db.session.commit()

    # Kirim OTP melalui email
    send_email(username, otp)

    return jsonify({"message": "OTP telah dikirim ke email"}), 200

def lupa_password():
    data = request.get_json()
    email = data.get('email')
    otp = data.get('otp')
    new_password = data.get('new_password')

    # Validasi input
    if not email or not otp or not new_password:
        return jsonify({"message": "Email, OTP, dan kata sandi baru diperlukan"}), 400

    # Cari pengguna sementara berdasarkan email
    temp_user = TemporaryUser.query.filter_by(username=email).first()
    if not temp_user:
        return jsonify({"message": "Email tidak ditemukan"}), 404

    # Cari pengguna permanen berdasarkan email
    user = User.query.filter_by(username=email).first()
    if not user:
        return jsonify({"message": "Pengguna tidak ditemukan"}), 404

    try:
        # Ubah password pengguna permanen
        user.password = generate_password_hash(new_password)
        
        # Hapus data pengguna sementara setelah berhasil
        db.session.delete(temp_user)

        # Commit perubahan ke database
        db.session.commit()

        return jsonify({"message": "Kata sandi berhasil diubah"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Terjadi kesalahan: {str(e)}"}), 500
