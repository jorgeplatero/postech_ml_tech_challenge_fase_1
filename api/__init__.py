import logging
from flask import Flask, jsonify, Blueprint, request
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from sqlalchemy import inspect

from api.config.config import Config
from api.models.__init__ import db
#from api.routes.auth import auth_bp, bcrypt
from api.routes.health import health_bp

#Imports só para Inicializar o banco
from api.models import scrapper_data
from api.models import users_access


from flask_bcrypt import Bcrypt

from api.models.user import db, User, get_user_by_username
from api.routes.auth import register_user, login

bcrypt = Bcrypt()
auth_bp = Blueprint('auth', __name__)
logger = logging.getLogger('api.auth')

def create_app():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('api')
    
    app = Flask(__name__)
    app.config.from_object(Config)

    #inicializa as extensões com o app
    db.init_app(app)
    jwt = JWTManager(app)
    swagger = Swagger(app)
    bcrypt.init_app(app) #inicialização da instância de bcrypt que está no auth.py

    #tratamento de erros do JWT
    @jwt.unauthorized_loader
    def unauthorized_callback(callback):
        if 'Missing' in str(callback) or 'Authorization header' in str(callback):
            return jsonify({'msg': 'Token não informado'}), 401
        return jsonify({'error': 'Erro de autenticação'}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(err):
        logger.error(f'Erro de token inválido: {err}')
        return jsonify({'error': 'Token inválido'}), 401

    @jwt.expired_token_loader
    def expired_token_callback(header, payload):
        return jsonify({'error': 'Token expirado'}), 401

    #registro de blueprints
    app.register_blueprint(auth_bp, url_prefix='/v1')
    app.register_blueprint(health_bp, url_prefix='/v1')

    #rota raiz
    @app.route('/')
    def home():
        return jsonify({
            'status': 'online',
            'msg': 'Bem-vindo à API.' 
        })
    #@auth_bp.route('/login', methods=['POST'])
    
    @app.route('/login', methods=['POST'])
    def login_route():
        data = request.get_json(force=True)

        username = data['username']
        password = data['password']

        return login(username, password)
    

    @app.route('/register', methods=['POST'])
    def register_route():
        data = request.get_json(force=True)

        username = data['username']
        password = data['password']

        return register_user(username, password)
    

    #criação das tabelas do db
    with app.app_context():
        try: 
            #o db.init_app(app) deve ser chamado antes desta linha
            db.create_all() 
            logger.info(f'Tabelas do banco de dados criadas/verificadas. {inspect(db.engine).get_table_names()}')
        except Exception as e:
            logger.error('Erro crítico ao criar as tabelas do BD: %s', e)

    return app