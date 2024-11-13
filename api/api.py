from flask import Blueprint
from flask_jwt_extended import jwt_required
from api.user import get_users, add_user, login_user
from api.profile import get_profile
from api.contact_us import contact_admin
from api.kacamata import get_kacamata, add_kacamata
from api.predict import get_prediction
from api.verify_token import verify_token

# Membuat Blueprint
api_blueprint = Blueprint('api', __name__)

# Daftarkan route ke Blueprint
api_blueprint.route('/verify_token', methods=['POST'])(jwt_required()(verify_token))

api_blueprint.route('/users', methods=['GET'])(jwt_required()(get_users))          
api_blueprint.route('/users', methods=['POST'])(add_user)                          
api_blueprint.route('/users/login', methods=['POST'])(login_user)                  # Endpoint login tidak perlu autentikasi
api_blueprint.route('/users/<int:user_id>/profile', methods=['GET'])(jwt_required()(get_profile))  
api_blueprint.route('/contact', methods=['POST'])(contact_admin)                   
api_blueprint.route('/kacamata', methods=['GET'])(jwt_required()(get_kacamata))    
api_blueprint.route('/kacamata', methods=['POST'])(jwt_required()(add_kacamata))   
api_blueprint.route('/predict', methods=['POST'])(get_prediction)  
