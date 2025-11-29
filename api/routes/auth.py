import logging
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from flask_bcrypt import Bcrypt
from api.models.user import db, User, get_user_by_username
from api.models.users_access import UserAccess


bcrypt = Bcrypt()
#auth_bp = Blueprint('auth', __name__)
logger = logging.getLogger('api.auth')

#@auth_bp.route('/register', methods=['POST'])
def register_user(username, password):
    '''
    Registra um novo usuário.
    ---
    parameters:
        - in: body
          name: body
          required: true
          schema:
            type: object
            properties:
                username:
                    type: string
                password:
                    type: string
    responses:
        201:
            description: Usuário criado com sucesso
        400:
            description: Usuário já existe
    '''

    #data = request.get_json(force=True)

    if get_user_by_username(username):
        return jsonify({'error': 'Usuário já existe'}), 400
    try:
        # hashed_password = bcrypt.generate_password_hash(password.decode('utf-8'))
        hashed_password = bcrypt.generate_password_hash(password) # Retirei o decode('utf-8') porque já é uma string
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logger.error('Erro ao registrar usuário: %s', e)
        return jsonify({'error': 'Erro interno ao registrar usuário'}), 500
    return jsonify({'msg': 'Usuário criado com sucesso'}), 201

#@auth_bp.route('/login', methods=['POST'])
def login(username, password):
    '''
    Gera um token JWT para autenticação.
    ---
    parameters:
        - in: body
          name: body
          required: true
          schema:
              type: object
              properties:
                  username:
                      type: string
                  password:
                      type: string
    responses:
        200:
            description: Login bem sucedido, retorna o token JWT
            schema:
                type: object
                properties:
                    access_token:
                        type: string
                        description: O token de acesso JWT
        401:
            description: Credenciais inválidas
    '''
    
    user = get_user_by_username(username)
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=str(user.id))

        # Salvando acessos do Usuário
        new_acess = UserAccess(
            username = username,
            token    = access_token)
        
        db.session.add(new_acess)
        db.session.commit()

        return jsonify({'access_token': access_token}), 200
    
    return jsonify({'error': 'Credenciais inválidas'}), 401