from sqlalchemy.orm import Session
from my_project.dao import director_dao, movie_dao
from my_project.domain.models import Director, Movie
from my_project.database import get_db

class DirectorNotFoundException(Exception):
    pass

class DirectorAlreadyExistsException(Exception):
    pass

def create_new_director(db: Session, director_schema):
    existing_director = director_dao.get_director_by_name(
        db, 
        director_schema.first_name, 
        director_schema.last_name,
        director_schema.imdb_code, 
        director_schema.nationality
    )
    if existing_director:
        raise DirectorAlreadyExistsException("Director already exists")
    
    return director_dao.create_director(db, director_schema)


def get_director_by_id(db: Session, director_id: int):
    director = director_dao.get_director(db, director_id)
    if not director:
        raise DirectorNotFoundException("Director not found")
    return director



def get_all_directors_service(db, skip=0, limit=100):
    return director_dao.get_all_directors(db, skip, limit)


def update_existing_director(db: Session, director_id: int, director_update):
    director = get_director_by_id(db, director_id)
    return director_dao.update_director(db, director, director_update)


def delete_existing_director(db: Session, director_id: int):
    director = get_director_by_id(db, director_id)
    director_dao.delete_director(db, director)


def get_movies_by_director_id(db: Session, director_id: int):
    director = get_director_by_id(db, director_id)
    return director.movies
