import logging
from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import create_access_token
from flask_bcrypt import Bcrypt
from api.models.scrapper_data import get_all_categories


bcrypt = Bcrypt()
#auth_bp = Blueprint('auth', __name__)
logger = logging.getLogger('api.auth')


def model_all_categories():
    '''
    Pega as categorias de Livros
    '''
    try:

        categorias = get_all_categories()

        if categorias:
            return make_response(categorias, 200)
        
        return make_response({"msg":"Sem categorias cadastradas"})
    
    except Exception as e:
        return make_response(jsonify({'error': e}), 401)
