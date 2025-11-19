
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from my_project.domain.models import Movie, Director


def get_movie_by_id(db, movie_id: int): 
    query = select(Movie).where(Movie.movie_id == movie_id)
    return db.scalars(query).first()

def get_movie_by_release_year(db, title: str, release_year: int):
    query = select(Movie).where(
        Movie.title == title,
        Movie.release_year == release_year
    )
    return db.scalars(query).first()


def get_all_movies(db, skip=0, limit=100):
    query = select(Movie).offset(skip).limit(limit)
    return db.scalars(query).all()


def get_movie_with_actors(db, movie_id: int):
    query = (
        select(Movie)
        .options(joinedload(Movie.actors))
        .where(Movie.movie_id == movie_id)
    )
    return db.scalars(query).first()


def create_movie(db, movie_schema):
    movie_data = movie_schema.model_dump()
    db_movie = Movie(**movie_data)

    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


def update_movie(db, db_movie, movie_update):
    update_data = movie_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_movie, key, value)

    db.commit()
    db.refresh(db_movie)
    return db_movie


def delete_movie(db, db_movie):
    db.delete(db_movie)
    db.commit()

def find_director_by_movie_id(db, movie_id: int):
    movie = get_movie_by_id(db, movie_id) 
    if movie and movie.director_id:
        director = db.scalars(select(Director).where(Director.director_id == movie.director_id)).first()
        return director
    return None