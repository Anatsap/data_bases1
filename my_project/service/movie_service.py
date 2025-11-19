
from my_project.dao import movie_dao


class MovieNotFoundException(Exception):
    pass


class MovieExistsException(Exception):
    pass


def create_new_movie(db, movie_schema):
    existing_movie = movie_dao.get_movie_by_release_year(
        db,
        movie_schema.title,
        movie_schema.release_year
    )

    if existing_movie:
        raise MovieExistsException("Movie exists")

    return movie_dao.create_movie(db, movie_schema)


def get_movie_by_id(db, movie_id):
    db_movie = movie_dao.get_movie_by_id(db, movie_id)

    if db_movie is None:
        raise MovieNotFoundException("Movie not found")

    return db_movie


def get_all_movies_service(db, skip, limit):
    return movie_dao.get_all_movies(db, skip, limit)


def update_existing_movie(db, movie_id, movie_update):
    db_movie = get_movie_by_id(db, movie_id)

    return movie_dao.update_movie(db, db_movie, movie_update)


def delete_existing_movie(db, movie_id):
    db_movie = get_movie_by_id(db, movie_id)

    movie_dao.delete_movie(db, db_movie)


def get_movie_actors_service(db, movie_id):
    db_movie = movie_dao.get_movie_with_actors(db, movie_id)

    if db_movie is None:
        raise MovieNotFoundException("Movie is not there")

    return db_movie

def get_movie_director_service(db, movie_id):
    db_director = movie_dao.find_director_by_movie_id(db, movie_id)
    return db_director