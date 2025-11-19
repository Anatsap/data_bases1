from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from pydantic import ValidationError
from my_project.database import get_db
from my_project.service.actor_service import (
    create_new_actor,
    get_all_actors_service,
    get_actor_by_id,
    update_existing_actor,
    delete_existing_actor,
    get_actor_movies_service,
    ActorNotFoundException,
    ActorAlreadyExistsException
)
from my_project.domain.schemas import ActorCreate, ActorUpdate, ActorResponse, MovieResponse

actor_bp = Blueprint('actors', __name__, url_prefix='/actors')

def with_db_session(f):
    def wrapper(*args, **kwargs):
        db = next(get_db())
        try:
            return f(db, *args, **kwargs)
        finally:
            db.close()
    wrapper.__name__ = f.__name__
    return wrapper

@actor_bp.route('/', methods=['POST'])
@with_db_session
def create_actor_endpoint(db: Session):
    try:
        actor_schema = ActorCreate.model_validate(request.json)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    
    try:
        new_actor = create_new_actor(db, actor_schema)
        return jsonify(ActorResponse.model_validate(new_actor).model_dump()), 201
    except ActorAlreadyExistsException as e:
        return jsonify({"error": str(e)}), 409

@actor_bp.route('/', methods=['GET'])
@with_db_session
def get_actors_endpoint(db: Session):
    actors = get_all_actors_service(db, skip=0, limit=100)
    response_data = [ActorResponse.model_validate(a).model_dump() for a in actors]
    return jsonify(response_data), 200

@actor_bp.route('/<int:actor_id>', methods=['GET'])
@with_db_session
def get_actor_endpoint(db: Session, actor_id: int):
    try:
        actor = get_actor_by_id(db, actor_id)
        return jsonify(ActorResponse.model_validate(actor).model_dump()), 200
    except ActorNotFoundException as e:
        return jsonify({"error": str(e)}), 404

@actor_bp.route('/<int:actor_id>', methods=['PUT'])
@with_db_session
def update_actor_endpoint(db: Session, actor_id: int):
    try:
        actor_update_schema = ActorUpdate.model_validate(request.json)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    
    try:
        updated_actor = update_existing_actor(db, actor_id, actor_update_schema)
        return jsonify(ActorResponse.model_validate(updated_actor).model_dump()), 200
    except ActorNotFoundException as e:
        return jsonify({"error": str(e)}), 404
    

@actor_bp.route('/<int:actor_id>', methods=['PATCH'])
@with_db_session
def patch_actor_endpoint(db: Session, actor_id: int):
    data = request.json  
    try:
        actor = get_actor_by_id(db, actor_id)
    except ActorNotFoundException as e:
        return jsonify({"error": str(e)}), 404
    if "name" in data:
        actor.name = data["name"]

    db.commit()
    db.refresh(actor)
    return jsonify(ActorResponse.model_validate(actor).model_dump()), 200


@actor_bp.route('/<int:actor_id>', methods=['DELETE'])
@with_db_session
def delete_actor_endpoint(db: Session, actor_id: int):
    try:
        delete_existing_actor(db, actor_id)
        return jsonify({"message": "Actor deleted"}), 200
    except ActorNotFoundException as e:
        return jsonify({"error": str(e)}), 404

@actor_bp.route('/<int:actor_id>/movies', methods=['GET'])
@with_db_session
def get_actor_movies_endpoint(db: Session, actor_id: int):
    try:
        actor_with_movies = get_actor_movies_service(db, actor_id)
        movies_data = [
            MovieResponse.model_validate(ma.movie).model_dump()  # беремо через .movie
            for ma in actor_with_movies.movies
        ]
        return jsonify(movies_data), 200
    except ActorNotFoundException as e:
        return jsonify({"error": str(e)}), 404
