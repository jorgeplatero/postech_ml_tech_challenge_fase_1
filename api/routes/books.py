import logging
from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import create_access_token
from flask_bcrypt import Bcrypt
from api.models.scrapper_data import get_all_books
from flask_jwt_extended import jwt_required


bcrypt = Bcrypt()
books_bp = Blueprint('books', __name__)
logger = logging.getLogger('api.auth')


@books_bp.route('/books', methods=['GET'])
@jwt_required()
def model_all_books():
    """
    Retorna a lista de todos os titulos de livros cadastrados no sistema.
    ---
    tags:
      - Livros
    responses:
      200:
        description: Lista do titulo dos livros ou mensagem de que não há livros.
        schema:
          type: array
          items:
            type: object
            properties:
              titulo:
                type: string
                description: Título principal do livro.
        examples:
          application/json: 
            - id: 101
              titulo: O Senhor dos Anéis
            - id: 102
              titulo: 1984
      401:
        description: Erro interno do servidor.
        schema:
          type: object
          properties:
            error:
              type: string
              description: Mensagem de erro capturada pela exceção.
    """
    try:

        books = get_all_books()

        if books:
            return make_response(books, 200)
        
        return make_response({"msg":"Sem livros cadastradas"})
    
    except Exception as e:
        return make_response(jsonify({'error': e}), 401)
