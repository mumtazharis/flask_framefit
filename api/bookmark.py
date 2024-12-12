from flask import request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from config import db
from models import Bookmark, User, Kacamata

def get_user_bookmarks():
    """Mengambil bookmark milik pengguna yang sedang login."""
    user_id = get_jwt_identity()  # Mendapatkan user_id dari JWT
    user_bookmarks = Bookmark.query.filter_by(user_id=user_id).all()

    if not user_bookmarks:
        return jsonify({'message': 'No bookmarks found for this user.'}), 404

    result = [
        {
            'bookmark_id': bookmark.bookmark_id,
            'kacamata_id': bookmark.kacamata_id,
            'kacamata_name': bookmark.kacamata.name if bookmark.kacamata else None
        }
        for bookmark in user_bookmarks
    ]
    return jsonify(result), 200

def add_bookmark():
    """Menambahkan bookmark baru untuk pengguna yang sedang login."""
    user_id = get_jwt_identity()  # Mendapatkan user_id dari JWT
    data = request.get_json()
    kacamata_id = data.get('kacamata_id')

    # Validasi input
    if not kacamata_id:
        return jsonify({'error': 'kacamata_id is required.'}), 400

    # Validasi kacamata
    kacamata = Kacamata.query.get(kacamata_id)
    if not kacamata:
        return jsonify({'error': 'Invalid kacamata_id.'}), 404

    # Tambahkan bookmark
    new_bookmark = Bookmark(user_id=user_id, kacamata_id=kacamata_id)
    db.session.add(new_bookmark)
    db.session.commit()
    return jsonify({'message': 'Bookmark added successfully.'}), 201

def delete_bookmark(kacamata_id):
    """Menghapus bookmark berdasarkan kacamata_id jika milik pengguna yang sedang login."""
    user_id = get_jwt_identity()  # Mendapatkan user_id dari JWT
    bookmark = Bookmark.query.filter_by(kacamata_id=kacamata_id, user_id=user_id).first()

    if not bookmark:
        return jsonify({'error': 'Bookmark not found or not authorized to delete.'}), 404

    db.session.delete(bookmark)
    db.session.commit()
    return jsonify({'message': 'Bookmark deleted successfully.'}), 200
