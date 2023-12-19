# IMPORTS
from utils import db
from flask_login import UserMixin

# TABELAS
class User(db.Model, UserMixin):
  __tablename__ = "user"
  id = db.Column(db.Integer, unique=True, primary_key=True)
  nome = db.Column(db.String(80), nullable=False)
  email = db.Column(db.String(80), nullable=False)
  resumo = db.Column(db.String(80), nullable=False)
  contato = db.Column(db.String(80), nullable=False)
  senha = db.Column(db.String(80), nullable=False)
  status = db.Column(db.Boolean, default=True)
  
  def __init__ (self, nome, email, resumo, contato, senha, status):
    self.nome = nome
    self.email = email
    self.resumo = resumo
    self.contato = contato
    self.senha = senha
    self.status = status
    
  def __repr__ (self):
    return f'User: {self.nome}.'

class Voluntario(db.Model):
   __tablename__ = "voluntario"
   id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, primary_key=True)
   cpf = db.Column(db.Integer, nullable=False)
  
   user = db.relationship('User', foreign_keys=id)

   def __init__(self, id, cpf):
     self.id = id
     self.cpf = cpf

   def __repr__(self):
     return f'Voluntário: {self.id}.'

class ONG(db.Model):
  __tablename__ = "ong"
  id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, primary_key=True)
  cnpj = db.Column(db.Integer, nullable=False)
  modalidade = db.Column(db.String(80), nullable=False)
  categoria = db.Column(db.String(80), nullable=False)
  cidade = db.Column(db.String(80), nullable=False)
  uf = db.Column(db.String(80), nullable=False)

  user = db.relationship('User', foreign_keys=id)
  
  def __init__ (self, id, cnpj, modalidade, categoria, cidade, uf):
    self.id = id
    self.cnpj = cnpj
    self.modalidade = modalidade
    self.categoria = categoria
    self.cidade = cidade
    self.uf = uf
    
  def __repr__ (self):
    return f'ONG: {self.id}.'

class Acao(db.Model):
  __tablename__ = "acao"
  id = db.Column(db.Integer, unique=True, primary_key=True)
  id_ong = db.Column(db.Integer, db.ForeignKey('ong.id'))
  id_volut = db.Column(db.Integer, db.ForeignKey('voluntario.id'))
  tipo = db.Column(db.String(80), nullable=False)
  
  ong = db.relationship('ONG', foreign_keys=id_ong)
  voluntario = db.relationship('Voluntario', foreign_keys=id_volut)
  
  def __init__ (self, id_ong, id_volut, tipo):
    self.id_ong = id_ong
    self.id_volut = id_volut
    self.tipo = tipo
    
  def __repr__ (self):
    return f'Ação: {self.id}.'

class Item(db.Model):
  __tablename__ = "item"
  id = db.Column(db.Integer, unique=True, primary_key=True)
  id_acao = db.Column(db.Integer, db.ForeignKey('acao.id'))
  valor = db.Column(db.Float, nullable=False)
  
  acao = db.relationship('Acao', foreign_keys=id_acao)
  
  def __init__ (self, id_acao, valor):
    self.id_acao = id_acao
    self.valor = valor
    
  def __repr__ (self):
    return f'Item: {self.id}.'

class Atuacao(db.Model):
  __tablename__ = "atuacao"
  id = db.Column(db.Integer, unique=True, primary_key=True)
  id_acao = db.Column(db.Integer, db.ForeignKey('acao.id'))
  area = db.Column(db.String(80), nullable=False)

  acao = db.relationship('Acao', foreign_keys=id_acao)

  def __init__ (self, id_acao, area):
    self.id_acao = id_acao
    self.area = area

  def __repr__ (self):
    return f'Atuação: {self.id}.'