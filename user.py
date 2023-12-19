# IMPORTS
from flask import jsonify, Blueprint, request
from models import User, Voluntario
from utils import lm
from flask_login import login_user, logout_user
import hashlib

# CONFIGS
bp_user = Blueprint("user", __name__)

# ROTAS

# LOGIN
@bp_user.route('/login', methods=['POST'])
def login():
  email = request.get_json().get('email')
  senha = hashlib.sha256(request.get_json().get('senha').encode()).hexdigest()

  if User.query.filter_by(email = email).filter_by(senha = senha).count() == 1:
    user = User.query.filter_by(email = email).first()
    
    if Voluntario.query.filter_by(id = user.id).count() == 1:
      login_user(user)
      
      response = {
        'status': 'success',
        'message': 'Bem-vindo(a)!',
        'id': user.id,
        'tipo': 'voluntario'
      }
      
      return jsonify(response), 200

    else:
      login_user(user)
      
      response = {
        'status': 'success',
        'message': 'Bem-vindo(a)!',
        'id': user.id,
        'tipo': 'ong'
      }

      return jsonify(response), 200
      
  else:
    response = {
      'status': 'alert',
      'message': 'Dados Incorretos!'
    }
      
    return jsonify(response), 200
  
# LOAD
@lm.user_loader
def load_user(id):
  u = User.query.filter_by(id=id).first()
  return u

# LOGOUT
@bp_user.route('/logout')
def logout():
	logout_user()