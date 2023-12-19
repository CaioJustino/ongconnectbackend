# IMPORTS
from flask import request, jsonify, Blueprint
from utils import db
from models import Acao, Item, Atuacao

# CONFIGS
bp_acao = Blueprint("acao", __name__)

# ROTAS

# GET
@bp_acao.route('/<int:id>', methods=['GET'])
def get(id):
  acao = Acao.query.get(id)
  
  if acao:
    if acao.tipo == "doacao":
      item = Item.query.filter_by(id_acao = acao.id).first()
      
      data = {
        'id': acao.id,
        'id_ong': acao.id_ong,
        'id_volut': acao.id_volut,
        'tipo': acao.tipo,
        'id_item': item.id,
        'valor': item.valor
      }

      response = {
        'status': 'success',
        'data': data,
      }

      return jsonify(response), 200
      
    else:
      atuacao = Atuacao.query.filter_by(id_acao = acao.id).first()
      
      data = {
        'id': acao.id,
        'id_ong': acao.id_ong,
        'id_volut': acao.id_volut,
        'tipo': acao.tipo,
        'id_atuacao': atuacao.id,
        'area': atuacao.area
      }

      response = {
        'status': 'success',
        'data': data,
      }

      return jsonify(response), 200
      
  else:
    response = {
      'message': 'Açao nao encontrada :('
    }

    return jsonify(response), 404

# CREATE
@bp_acao.route('/cadastro', methods=['POST'])
def create():
  id_ong = request.get_json().get('id_ong')
  id_volut = request.get_json().get('id_volut')
  tipo = request.get_json().get('tipo')
    
  if tipo == "doacao":
    valor = request.get_json().get('valor')
    new_acao = Acao(id_ong, id_volut, tipo)
    db.session.add(new_acao)
    db.session.commit()
    new_item = Item(new_acao.id, valor)
    db.session.add(new_item)
    db.session.commit()

    response = {
      'status': 'success',
      'message': 'Açao realizada!',
    }

    return jsonify(response), 200
    
  else:
    area = request.get_json().get('area')
    new_acao = Acao(id_ong, id_volut, tipo)
    db.session.add(new_acao)
    db.session.commit()
    new_atuacao = Atuacao(new_acao.id, area)
    db.session.add(new_atuacao)
    db.session.commit()

    response = {
      'status': 'success',
      'message': 'Açao realizada!',
    }

    return jsonify(response), 200

# UPDATE
@bp_acao.route('/editar/<int:id>', methods=['PUT'])
def update(id):
  acao = Acao.query.get(id)
  
  if acao:
    if acao.tipo == "doacao":
      item = Item.query.filter_by(id_acao = acao.id).first()
      acao.id_ong = request.get_json().get('id_ong')
      acao.id_volut = request.get_json().get('id_volut')
      acao.tipo = request.get_json().get('tipo')
      item.valor = request.get_json().get('valor')

      db.session.commit()

      response = {
        'status': 'success',
        'message': 'Açao atualizada!',
      }

      return jsonify(response), 200
      
    else:
      atuacao = Atuacao.query.filter_by(id_acao = acao.id).first()
      acao.id_ong = request.get_json().get('id_ong')
      acao.id_volut = request.get_json().get('id_volut')
      acao.tipo = request.get_json().get('tipo')
      atuacao.area = request.get_json().get('atuacao')
      
      db.session.commit()

      response = {
        'status': 'success',
        'message': 'Açao atualizada!',
      }

      return jsonify(response), 200
  
  else:
    response = {
      'message': 'Açao nao encontrada :('
    }

    return jsonify(response), 404