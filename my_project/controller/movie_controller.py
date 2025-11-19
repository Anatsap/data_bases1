from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from sqlalchemy.orm import Session
from my_project.database import get_db
from my_project.service import movie_service
from my_project.service.movie_service import MovieNotFoundException, MovieExistsException
from my_project.domain.schemas import MovieCreate, MovieUpdate, MovieResponse, ActorResponse, DirectorResponse
from sqlalchemy.orm import joinedload
from my_project.service.movie_service import (
    create_new_movie,
    get_all_movies_service,
    get_movie_by_id,
    update_existing_movie,
    delete_existing_movie,
    get_movie_actors_service,
    get_movie_director_service,
    MovieNotFoundException,
    MovieExistsException
)
from my_project.domain.schemas import MovieCreate, MovieUpdate, MovieResponse, ActorResponse

movie_bp = Blueprint('movies', __name__, url_prefix='/movies')

def with_db_session(f):
    def wrapper(*args, **kwargs):
        db = next(get_db())
        try:
            return f(*args, db=db, **kwargs)
        finally:
            db.close()
    wrapper.__name__ = f.__name__
    return wrapper

@movie_bp.route('/', methods=['POST'])
@with_db_session
def create_movie_endpoint(db: Session):
    try:
        movie_schema = MovieCreate.model_validate(request.json)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    
    try:
        new_movie = create_new_movie(db, movie_schema)
        return jsonify(MovieResponse.model_validate(new_movie).model_dump()), 201
    except MovieExistsException as error:
        return jsonify({"error": str(error)}), 409

@movie_bp.route('/', methods=['GET'])
@with_db_session
def get_movies_endpoint(db: Session):
    movies = get_all_movies_service(db, skip=0, limit=100)
    response_data = []
    for m in movies:
        movie_dict = MovieResponse.model_validate(m).model_dump()
        if m.director:
            movie_dict['director'] = {
                "director_id": m.director.director_id,
                "first_name": m.director.first_name,
                "last_name": m.director.last_name
            }
        response_data.append(movie_dict)
    return jsonify(response_data), 200

@movie_bp.route('/<int:movie_id>', methods=['GET'])
@with_db_session
def get_movie_endpoint(db: Session, movie_id: int):
    try:
        movie = get_movie_by_id(db, movie_id)
        movie_dict = MovieResponse.model_validate(movie).model_dump()
        if movie.director:
            movie_dict['director'] = {
                "director_id": movie.director.director_id,
                "first_name": movie.director.first_name,
                "last_name": movie.director.last_name
            }
        return jsonify(movie_dict), 200
    except MovieNotFoundException as e:
        return jsonify({"error": str(e)}), 404

@movie_bp.put('/<int:movie_id>')
@with_db_session
def update_movie_endpoint(db, movie_id):
    db = next(get_db())
    try:
        content = request.get_json()
        movie_update_schema = MovieUpdate.model_validate(content)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
        
    try:
        updated_movie = update_existing_movie(db, movie_id, movie_update_schema)
        return jsonify(MovieResponse.model_validate(updated_movie).model_dump()), 200
    except MovieNotFoundException as e:
        return jsonify({"error": str(e)}), 404

@movie_bp.route('/<int:movie_id>', methods=['PATCH'])
@with_db_session
def patch_movie_endpoint(db: Session, movie_id: int):
    try:
        content = request.get_json()
        movie_update_schema = MovieUpdate.model_validate(content)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    
    try:
        updated_movie = update_existing_movie(db, movie_id, movie_update_schema)
        return jsonify(MovieResponse.model_validate(updated_movie).model_dump()), 200
    except MovieNotFoundException as e:
        return jsonify({"error": str(e)}), 404


@movie_bp.delete('/<int:movie_id>')
@with_db_session
def delete_movie_endpoint(db: Session, movie_id: int):
    try:
        delete_existing_movie(db, movie_id)
        return jsonify({"message": "Movie deleted"}), 200
    except MovieNotFoundException as e:
        return jsonify({"error": str(e)}), 404

@movie_bp.route('/<int:movie_id>/actors', methods=['GET'])
@with_db_session
def get_movie_actors_endpoint(db: Session, movie_id: int):
    try:
        movie_with_actors = get_movie_actors_service(db, movie_id)
        actors_data = [
            ActorResponse.model_validate(ma.actor).model_dump()  
            for ma in movie_with_actors.actors
        ]
        return jsonify(actors_data), 200
    except MovieNotFoundException as e:
        return jsonify({"error": str(e)}), 404


@movie_bp.route('/<int:movie_id>/director', methods=['GET'])
@with_db_session
def get_movie_director_endpoint(db: Session, movie_id: int):
    try:
        director = get_movie_director_service(db, movie_id) 
        if director:
            return jsonify(DirectorResponse.model_validate(director).model_dump()), 200
        return jsonify({"error": "Director not assigned to this movie"}), 404 
    
    except MovieNotFoundException as e:
        return jsonify({"error": str(e)}), 404
