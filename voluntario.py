# IMPORTS
from flask import request, jsonify, Blueprint
from utils import db
from models import User, Voluntario, ONG, Acao
from flask_login import logout_user
import hashlib

# CONFIGS
bp_volut = Blueprint("voluntario", __name__)

# ROTAS

# GET
@bp_volut.route('/<int:id>', methods=['GET'])
def get(id):
  user = User.query.get(id)
  volut = Voluntario.query.get(id)
  
  if volut:
    data = {
      'id': user.id,
      'nome': user.nome,
      'email': user.email,
      'resumo': user.resumo,
      'contato': user.contato,
      'cpf': volut.cpf
    }
    
    response = {
      'status': 'success',
      'message': 'Voluntario encontrado!',
      'data': data,
    }
    
    return jsonify(response), 200

  else:
    response = {
      'status': 'danger',
      'message': 'Voluntario nao encontrado :('
    }
    
    return jsonify(response), 404

# CREATE
@bp_volut.route('/cadastro', methods=['POST'])
def create():
  nome = request.get_json().get('nome')
  email = request.get_json().get('email')
  resumo = request.get_json().get('resumo')
  contato = request.get_json().get('contato')
  cpf = request.get_json().get('cpf')
  senha = hashlib.sha256(request.get_json().get('senha').encode()).hexdigest()

  if User.query.filter_by(email = email).count() == 1:
    response = {
      'status': 'danger',
      'message': 'E-mail indisponivel!',
    }

    return jsonify(response), 200
    
  else:
    new_user = User(nome, email, resumo, contato, senha, True)
    db.session.add(new_user)
    db.session.commit()
    new_client = Voluntario(new_user.id, cpf)
    db.session.add(new_client)
    db.session.commit()
  
    response = {
      'status': 'success',
      'message': 'Voluntario criado!',
    }
      
    return jsonify(response), 200

# UPDATE
@bp_volut.route('/editar/<int:id>', methods=['PUT'])
def update(id):
  user = User.query.get(id)
  volut = Voluntario.query.get(id)
  
  if volut:
    user.nome = request.get_json().get('nome')
    user.email = request.get_json().get('email')
    user.resumo = request.get_json().get('resumo')
    user.contato = request.get_json().get('contato')
    volut.cpf = request.get_json().get('cpf')
    user.senha = hashlib.sha256(request.get_json().get('senha').encode()).hexdigest()

    if User.query.filter_by(email = user.email).filter(id != user.id).count() == 1:
      response = {
        'status': 'danger',
        'message': 'E-mail indisponivel!',
      }

      return jsonify(response), 200

    else:
      db.session.commit()
      
      response = {
        'status': 'success',
        'message': 'Voluntario atualizado!',
      }
    
      return jsonify(response), 200

  else:
    response = {
      'status': 'danger',
      'message': 'Voluntario nao encontrado :('
    }
    
    return jsonify(response), 404

# DELETE
@bp_volut.route('/desativar/<int:id>', methods=['PUT'])
def delete(id):
  user = User.query.get(id)
  volut = Voluntario.query.get(id)
  
  if volut:
    user.status = False
    db.session.commit()
    logout_user()

    response = {
      'status': 'success',
      'message': 'Cadastro desativado!',
    }
  
    return jsonify(response), 200
  
  else:
    response = {
      'status': 'danger',
      'message': 'Voluntario nao encontrado :('
    }
    
    return jsonify(response), 404

# GET ONGS
@bp_volut.route('/ongs/<int:id>', methods=['GET'])
def get_ongs(id):
  ongs = db.session.query(User, ONG, Acao).join(User, ONG.id == User.id).join(Acao, ONG.id == Acao.id_ong).filter(Acao.id_volut == id).order_by(ONG.id.desc()).all()
  
  if ongs:
    for user, ong in ongs:
      data = {
        'id': user.id,
        'nome': user.nome,
        'email': user.email,
        'resumo': user.resumo,
        'contato': user.contato,
        'cnpj': ong.cnpj,
        'modalidade': ong.modalidade,
        'categoria': ong.categoria,
        'cidade': ong.cidade,
        'uf': ong.uf
      }
  
    response = {
      'status': 'success',
      'data': data,
    }

    return jsonify(response), 200

  else:
    response = {
      'message': 'ONGs nao encontradas :('
    }

    return jsonify(response), 200