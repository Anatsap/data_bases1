from typing import List, Dict, Any
from flask import Blueprint, jsonify, Response, request
from http import HTTPStatus
from sqlalchemy.orm import Session
from my_project.domain.models import Director
from my_project.service import director_service
from my_project.domain.schemas import DirectorCreate, DirectorUpdate, DirectorResponse, MovieResponse
from pydantic import ValidationError
from my_project.database import get_db

director_bp = Blueprint('directors', __name__, url_prefix='/directors')

@director_bp.get('')
def get_all_directors():
    db = next(get_db())
    directors = director_service.get_all_directors_service(db)
    response_data = [DirectorResponse.model_validate(d).model_dump() for d in directors]
    return jsonify(response_data), HTTPStatus.OK

@director_bp.route('/', methods=['POST'])
def create_director():
    db = next(get_db())
    try:
        content = request.get_json()
        director_schema = DirectorCreate.model_validate(content)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), HTTPStatus.BAD_REQUEST

    new_director = director_service.create_new_director(db, director_schema)
    return jsonify(DirectorResponse.model_validate(new_director).model_dump()), HTTPStatus.CREATED

@director_bp.get('/<int:director_id>')
def get_director(director_id: int) -> Response:
    director = director_service.get_director_by_id(director_id)
    return jsonify(DirectorResponse.model_validate(director).model_dump()), HTTPStatus.OK

@director_bp.route('/<int:director_id>', methods=['PUT']) 
def update_director(director_id: int):
    db = next(get_db())
    try:
        content = request.get_json()
        director_update_schema = DirectorUpdate.model_validate(content)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), HTTPStatus.BAD_REQUEST

    updated_director = director_service.update_existing_director(db, director_id, director_update_schema)
    return jsonify(DirectorResponse.model_validate(updated_director).model_dump()), HTTPStatus.OK

@director_bp.patch('/<int:director_id>')
def patch_director(director_id: int) -> Response:
    db = next(get_db())
    content = request.get_json()
    updated_director = director_service.update_existing_director(db, director_id, DirectorUpdate.model_validate(content))
    
    return jsonify(DirectorResponse.model_validate(updated_director).model_dump()), HTTPStatus.OK

@director_bp.delete('/<int:director_id>')
def delete_director(director_id: int) -> Response:
    db = next(get_db())
    director_service.delete_existing_director(db, director_id)
    return jsonify({"message": "Director deleted"}), HTTPStatus.OK

@director_bp.get('/<int:director_id>/movies')
def get_director_movies(director_id: int) -> Response:
    db = next(get_db())
    movies_data = director_service.get_movies_by_director_id(db, director_id)
    response_data = [MovieResponse.model_validate(m).model_dump() for m in movies_data]
    return jsonify(response_data), HTTPStatus.OK





