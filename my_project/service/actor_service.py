
from sqlalchemy.orm import Session
from my_project.dao import actor_dao, movie_dao
from my_project.domain.models import Actor, MovieActor
from my_project.dao.actor_dao import get_actor
from sqlalchemy import select
from sqlalchemy.orm import selectinload
class ActorNotFoundException(Exception):
    pass

class ActorAlreadyExistsException(Exception):
    pass


def create_new_actor(db: Session, actor_schema):
    existing_actor = actor_dao.get_actor_by_name(
        db,
        actor_schema.last_name,
        actor_schema.birth_date,
        actor_schema.nationality,
        actor_schema.bio,
        actor_schema.imdb_code
    )
    if existing_actor:
        raise ActorAlreadyExistsException("Actor already exists")
    
    return actor_dao.create_actor(db, actor_schema)


def get_actor_by_id(db: Session, actor_id: int):
    actor = actor_dao.get_actor(db, actor_id)
    if not actor:
        raise ActorNotFoundException("Actor not found")
    return actor


def get_all_actors_service(db: Session, skip=0, limit=100):
    return actor_dao.get_all_actors(db, skip, limit)


def update_existing_actor(db: Session, actor_id: int, actor_update):
    actor = get_actor_by_id(db, actor_id)
    return actor_dao.update_actor(db, actor, actor_update)


def delete_existing_actor(db: Session, actor_id: int):
    actor = get_actor_by_id(db, actor_id)
    actor_dao.delete_actor(db, actor)


def get_movies_by_actor_id(db: Session, actor_id: int):
    actor = get_actor_by_id(db, actor_id)
    return [ma.movie for ma in actor.movies]

def get_actor_movies_service(db, actor_id: int):
    actor = db.scalars(
        select(Actor)
        .where(Actor.actor_id == actor_id)
        .options(selectinload(Actor.movies))  
    ).first()

    if not actor:
        raise ActorNotFoundException(f"Actor with id {actor_id} not found")

    return actor
