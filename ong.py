# IMPORTS
from flask import request, jsonify, Blueprint
from utils import db
from models import User, ONG, Voluntario, Acao
from flask_login import logout_user
import hashlib

# CONFIGS
bp_ong = Blueprint("ong", __name__)

# ROTAS

# GET
@bp_ong.route('/<int:id>', methods=['GET'])
def get(id):
  user = User.query.get(id)
  ong = ONG.query.get(id)
  
  if ong:
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
      'message': 'ONG encontrada!',
      'data': data,
    }
    
    return jsonify(response), 200

  else:
    response = {
      'message': 'ONG nao encontrada :('
    }
    
    return jsonify(response), 404

# CREATE
@bp_ong.route('/cadastro', methods=['POST'])
def create():
  nome = request.get_json().get('nome')
  email = request.get_json().get('email')
  resumo = request.get_json().get('resumo')
  contato = request.get_json().get('contato')
  cnpj = request.get_json().get('cnpj')
  modalidade = request.get_json().get('modalidade')
  categoria = request.get_json().get('categoria')
  cidade = request.get_json().get('cidade')
  uf = request.get_json().get('uf')
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
    new_ong = ONG(new_user.id, cnpj, modalidade, categoria, cidade, uf)
    db.session.add(new_ong)
    db.session.commit()
    
    response = {
      'status': 'success',
      'message': 'ONG criada!',
    }
      
    return jsonify(response), 200

# UPDATE
@bp_ong.route('/editar/<int:id>', methods=['PUT'])
def update(id):
  user = User.query.get(id)
  ong = ONG.query.get(id)
  
  if ong:
    user.nome = request.get_json().get('nome')
    user.email = request.get_json().get('email')
    user.resumo = request.get_json().get('resumo')
    user.contato = request.get_json().get('contato')
    ong.cnpj = request.get_json().get('cnpj')
    ong.modalidade = request.get_json().get('modalidade')
    ong.categoria = request.get_json().get('categoria')
    ong.cidade = request.get_json().get('cidade')
    ong.uf = request.get_json().get('uf')
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
        'message': 'ONG atualizada!',
      }
    
      return jsonify(response), 200

  else:
    response = {
      'message': 'ONG nao encontrada :('
    }
    
    return jsonify(response), 404

# DELETE
@bp_ong.route('/desativar/<int:id>', methods=['PUT'])
def delete(id):
  user = User.query.get(id)
  ong = ONG.query.get(id)
  
  if ong:
    user.status = False
    db.session.commit()
    logout_user()
    
    response = {
      'status': 'success',
      'message': 'ONG deletada!',
    }
  
    return jsonify(response), 200
  
  else:
    response = {
      'message': 'ONG nao encontrada :('
    }
    
    return jsonify(response), 404

# GET VOLUTS
@bp_ong.route('/voluntarios/<int:id>', methods=['GET'])
def get_voluts(id):
  voluts = db.session.query(User, Voluntario, Acao).join(User, Voluntario.id == User.id).join(Acao, Voluntario.id == Acao.id_volut).filter(Acao.id_ong == id).order_by(Voluntario.id.desc()).all()

  if voluts:
    for user, voluntario in voluts:
      data = {
        'id': user.id,
        'nome': user.nome,
        'email': user.email,
        'resumo': user.resumo,
        'contato': user.contato,
        'cpf': voluntario.cpf
      }

    response = {
      'status': 'success',
      'data': data,
    }

    return jsonify(response), 200

  else:
    response = {
      'message': 'Voluntarios nao encontrados :('
    }

    return jsonify(response), 200