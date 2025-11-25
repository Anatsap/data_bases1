from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from sqlalchemy.orm import Session, joinedload
from my_project.database import get_db
from my_project.service.movie_service import (
    create_new_movie,
    get_all_movies_service,
    get_movie_by_id,
    update_existing_movie,
    delete_existing_movie,
    get_movies_with_facts,
    MovieNotFoundException,
    MovieExistsException
)
from my_project.domain.models import Movie
from my_project.domain.schemas import MovieCreate, MovieUpdate, MovieResponse, ActorResponse, DirectorResponse, MovieWithFactsResponse, MovieFactResponse

from http import HTTPStatus 

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
        return jsonify({"error": e.errors()}), HTTPStatus.BAD_REQUEST
    
    try:
        new_movie = create_new_movie(db, movie_schema)
        return jsonify(MovieResponse.model_validate(new_movie).model_dump()), HTTPStatus.CREATED
    except MovieExistsException as error:
        return jsonify({"error": str(error)}), HTTPStatus.CONFLICT

@movie_bp.route('/', methods=['GET'])
@with_db_session
def get_movies_endpoint(db: Session):
    movies = get_all_movies_service(db, skip=0, limit=100)
    response_data = []
    
    for m in movies:
        movie_dict = MovieResponse.model_validate(m).model_dump()        
        response_data.append(movie_dict)
    return jsonify(response_data), HTTPStatus.OK

@movie_bp.route('/<int:movie_id>', methods=['GET'])
@with_db_session
def get_movie_endpoint(db: Session, movie_id: int):
    try:
        movie = get_movie_by_id(db, movie_id)
        movie_dict = MovieResponse.model_validate(movie).model_dump()
        
        if movie.directors:
            movie_dict['directors'] = [
                DirectorResponse.model_validate(d).model_dump()
                for d in movie.directors
            ]

        return jsonify(movie_dict), HTTPStatus.OK
    except MovieNotFoundException as e:
        return jsonify({"error": str(e)}), HTTPStatus.NOT_FOUND

@movie_bp.put('/<int:movie_id>')
@with_db_session
def update_movie_endpoint(db: Session, movie_id: int): 
    try:
        content = request.get_json()
        movie_update_schema = MovieUpdate.model_validate(content)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), HTTPStatus.BAD_REQUEST
        
    try:
        updated_movie = update_existing_movie(db, movie_id, movie_update_schema)
        return jsonify(MovieResponse.model_validate(updated_movie).model_dump()), HTTPStatus.OK
    except MovieNotFoundException as e:
        return jsonify({"error": str(e)}), HTTPStatus.NOT_FOUND

@movie_bp.route('/<int:movie_id>', methods=['PATCH'])
@with_db_session
def patch_movie_endpoint(db: Session, movie_id: int):
    try:
        content = request.get_json()
        movie_update_schema = MovieUpdate.model_validate(content)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), HTTPStatus.BAD_REQUEST
    
    try:
        updated_movie = update_existing_movie(db, movie_id, movie_update_schema)
        return jsonify(MovieResponse.model_validate(updated_movie).model_dump()), HTTPStatus.OK
    except MovieNotFoundException as e:
        return jsonify({"error": str(e)}), HTTPStatus.NOT_FOUND


@movie_bp.delete('/<int:movie_id>')
@with_db_session
def delete_movie_endpoint(db: Session, movie_id: int):
    try:
        delete_existing_movie(db, movie_id)
        return jsonify({"message": "Movie deleted"}), HTTPStatus.OK
    except MovieNotFoundException as e:
        return jsonify({"error": str(e)}), HTTPStatus.NOT_FOUND

@movie_bp.route('/<int:movie_id>/actors', methods=['GET'])
@with_db_session
def get_movie_actors_endpoint(db: Session, movie_id: int):
    try:
        movie = get_movie_by_id(db, movie_id, options=joinedload(Movie.actors))
        
        actors_data = [
            ActorResponse.model_validate(ma).model_dump()  
            for ma in movie.actors
        ]
        return jsonify(actors_data), HTTPStatus.OK
    except MovieNotFoundException as e:
        return jsonify({"error": str(e)}), HTTPStatus.NOT_FOUND


@movie_bp.route('/<int:movie_id>/directors', methods=['GET']) 
@with_db_session
def get_movie_directors_endpoint(db: Session, movie_id: int):
    try:
        movie = get_movie_by_id(db, movie_id, options=joinedload(Movie.directors))
        
        if not movie.directors:
            return jsonify({"error": "No directors assigned to this movie"}), HTTPStatus.NOT_FOUND

        directors_data = [
            DirectorResponse.model_validate(d).model_dump()
            for d in movie.directors
        ]
        return jsonify(directors_data), HTTPStatus.OK
    
    except MovieNotFoundException as e:
        return jsonify({"error": str(e)}), HTTPStatus.NOT_FOUND


@movie_bp.get('/movies-grouped-details') 
@with_db_session
def get_movies_grouped_details_endpoint(db: Session):
    movies = get_all_movies_service(db, skip=0, limit=100)
    response_dict = {}    
    for m in movies:
        movie_title = m.title
        directors_list = []
        if m.directors:
            directors_list = [
                DirectorResponse.model_validate(d).model_dump()
                for d in m.directors
            ]
        movie_base_data = MovieResponse.model_validate(m).model_dump()
        
        response_dict[movie_title] = {
            "movie_details": movie_base_data,
            "directors": directors_list
        }
            
    return jsonify(response_dict), HTTPStatus.OK


@movie_bp.get('/movies-with-facts') 
@with_db_session
def get_movies_with_facts_endpoint(db: Session):
    movies = get_movies_with_facts(db, skip=0, limit=100) 
    
    response_data = []
    for m in movies:
        movie_data = MovieWithFactsResponse.model_validate(m).model_dump()
        response_data.append(movie_data)
        
    return jsonify(response_data), HTTPStatus.OK




# У my_project/controller/movie_controller.py

@movie_bp.get('/movies-facts-grouped') 
@with_db_session
def get_movies_facts_grouped_endpoint(db: Session):
    from my_project.service.movie_service import get_movies_with_facts 
    movies = get_movies_with_facts(db, skip=0, limit=100)
    response_dict = {}    
    for m in movies:
        movie_key = f"Movie title : {m.title}"
        facts_list = []
        if m.movie_facts:
            facts_list = [
                {   
                    "id": f.fact_id,        
                    "fact_text": f.fact_text
                }
                for f in m.movie_facts
            ]
            response_dict[movie_key] = facts_list
            
    return jsonify(response_dict), HTTPStatus.OK


@movie_bp.get('/movies-facts-list') 
@with_db_session
def get_movies_facts_list_endpoint(db: Session):
    from my_project.service.movie_service import get_movies_with_facts
    movies = get_movies_with_facts(db, skip=0, limit=100)
    
    response_data = [] 
    
    for m in movies:
        facts_list = []
        if m.movie_facts:
            facts_list = [
                f.fact_text 
                for f in m.movie_facts
            ]
        
        movie_entry = {
            "movie_title": m.title, 
            "facts": facts_list      
        }
        
        response_data.append(movie_entry)
            
    return jsonify(response_data), HTTPStatus.OK