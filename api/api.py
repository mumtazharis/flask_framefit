from flask import Blueprint
from flask_jwt_extended import jwt_required
from api.user import register, login_user, send_otp
from api.profile import get_profile
from api.contact_us import contact_admin
from api.kacamata import get_kacamata, add_kacamata, get_rekomendasi
# from api.predict import get_prediction
from api.predictpcvk import get_prediction
from api.token import verify_token, refresh_token
from api.profile import get_profile
# Membuat Blueprint
api_blueprint = Blueprint('api', __name__)

# Daftarkan route ke Blueprint
api_blueprint.route('/verify_token', methods=['POST'])(jwt_required()(verify_token))       
api_blueprint.route('/refresh_token', methods=['POST'])(jwt_required(refresh=True)(refresh_token))       
api_blueprint.route('/users/register', methods=['POST'])(register)                          
api_blueprint.route('/users/sendotp', methods=['POST'])(send_otp)                          
api_blueprint.route('/users/login', methods=['POST'])(login_user)               
api_blueprint.route('/profile', methods=['GET'])(jwt_required()(get_profile))              
api_blueprint.route('/contact', methods=['POST'])(contact_admin)                   
api_blueprint.route('/kacamata', methods=['GET'])(jwt_required()(get_kacamata))    
api_blueprint.route('/kacamata', methods=['POST'])(jwt_required()(add_kacamata))   
api_blueprint.route('/rekomendasi_kacamata', methods=['GET'])(get_rekomendasi)   
api_blueprint.route('/predict', methods=['POST'])(get_prediction)  

