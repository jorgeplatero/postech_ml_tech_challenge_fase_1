import logging
from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import create_access_token
from flask_bcrypt import Bcrypt
from api.models.scrapper_data import get_all_categories
from flask_jwt_extended import jwt_required


bcrypt = Bcrypt()
categories_bp = Blueprint('categories', __name__)
logger = logging.getLogger('api.auth')


@categories_bp.route('/categories', methods=['GET'])
@jwt_required()
def model_all_categories():
    """
    Retorna a lista de todas as categorias de livros.
    ---
    tags:
      - Categorias
    responses:
      200:
        description: Lista de categorias ou mensagem de que não há categorias.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: ID da categoria.
              nome:
                type: string
                description: Nome da categoria.
        examples:
          application/json: 
            - id: 1
              nome: Ficção Científica
            - id: 2
              nome: Romance
            - id: 3
              nome: Fantasia
      401:
        description: Erro interno ou de autenticação (se aplicável na exceção).
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensagem de erro.
    """
    try:

        categorias = get_all_categories()

        if categorias:
            return make_response(categorias, 200)
        
        return make_response({"msg":"Sem categorias cadastradas"})
    
    except Exception as e:
        return make_response(jsonify({'error': e}), 401)
