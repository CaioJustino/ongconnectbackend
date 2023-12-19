# IMPORTS
from flask import Flask, jsonify, url_for, session
from flask_migrate import Migrate
from flask_oauthlib.client import OAuth
from flask_cors import CORS
from flask_login import login_user, logout_user

# UTILS
from utils import db, lm
from models import User, Voluntario

# CONTROLLERS
from controllers.user import bp_user
from controllers.voluntario import bp_volut
from controllers.ong import bp_ong
from controllers.acao import bp_acao

# CONFIGS
app = Flask(__name__)
app.secret_key = "0NGcoNn3ct"
CORS(app, resources={r"/*": {"origins": "*"}})
CORS(app, resources={r"/*": {"origins": "https://ongconnectfrontend.caio-victorvic4.repl.co", "allow_headers":"Acess-Control-Allow-Origin"}})

# BLUEPRINTS
app.register_blueprint(bp_user)
app.register_blueprint(bp_volut, url_prefix='/voluntario')
app.register_blueprint(bp_ong, url_prefix='/ong')
app.register_blueprint(bp_acao, url_prefix='/acao')

# DATABASE
# conexao = "mysql+pymysql://root@localhost/ongconnect"
conexao = "sqlite:///ongconnect.db"
app.config['SQLALCHEMY_DATABASE_URI'] = conexao
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# MIGRATE
migrate = Migrate(app, db)

# LOGIN MANAGER
lm.init_app(app)

# OAUTH
oauth = OAuth(app)
cors = CORS(app)

# OAUTH - GOOGLE
google = oauth.remote_app(
  "google",
  consumer_key="527387702653-7t7kp7l499h6to37ba9qjlhi6kef4m2s.apps.googleusercontent.com",
  consumer_secret="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",
  request_token_params={
      "scope": ["profile", "email"]
  },
  base_url="https://www.googleapis.com/oauth2/v1/",
  request_token_url=None,
  access_token_method="POST",
  access_token_url="https://accounts.google.com/o/oauth2/token",
  authorize_url="https://accounts.google.com/o/oauth2/auth",
)

# LOGIN
@app.route("/login/google")
def login_google():
  return google.authorize(callback=url_for("auth_google", _external=True))

# AUTHORIZED
@app.route("/auth/google")
def auth_google():
  resp = google.authorized_response()
  session["google_token"] = (resp["access_token"], "")
  user_info = google.get("userinfo")

  if User.query.filter_by(email = user_info.data.get("email")).count() == 1:
    user = User.query.filter_by(email=user_info.data["email"]).first()
    
    if Voluntario.query.filter_by(id = user.id).count() == 1:
      login_user(user)
      response = {
        'status': 'success',
        'message': 'Bem-vindo(a)!',
        'id': user.id,
        'email': user_info.data.get("email"),
        'tipo': 'voluntario'
      }

      return jsonify(response), 200

    else:
      login_user(user)
      response = {
        'status': 'success',
        'message': 'Bem-vindo(a)!',
        'id': user.id,
        'email': user_info.data.get("email"),
        'tipo': 'ong'
      }

      return jsonify(response), 200

  else:
    response = {
      'status': 'danger',
      'message': 'Dados Incorretos!'
    }

    return jsonify(response), 200

# LOGOUT
@app.route("/logout/google")

def logout_google():
  session.pop("google_token", None)
  logout_user()
  response = {
    'status': 'success',
    'message': 'Deslogado!'
  }
  return jsonify(response), 200

@google.tokengetter
def get_google_oauth_token():
  return session.get("google_token")

# ERROR EXCEPTIONS
@app.errorhandler(500)
def all_exception_handler(e):
  response = {
    'message': 'Internal Server Error :('
  }
  return jsonify(response), 500

@app.errorhandler(404)
def not_found(e):
  response = {
    'message': 'Pagina nao encontrada :('
  }
  return jsonify(response), 404

@app.errorhandler(401)
def unathorized(e):
  response = {
    'message': 'Acesso negado :('
  }
  return jsonify(response), 401

app.run(host='0.0.0.0', port=80)