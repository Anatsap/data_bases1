from sqlalchemy import select
from my_project.domain.models import Director


def get_director(db, director_id: int):
    query = select(Director).where(Director.director_id == director_id)
    return db.scalars(query).first()


def get_director_by_imdb(db, imdb_code: str):
    query = select(Director).where(Director.imdb_code == imdb_code)
    return db.scalars(query).first()


def get_director_by_name(db, first_name: str, last_name: str, nationality:str, imdb_code:str):
    query = select(Director).where(
        Director.first_name == first_name,
        Director.last_name == last_name,
        Director.nationality == nationality,
        Director.imdb_code == imdb_code
    )
    return db.scalars(query).first()


def get_all_directors(db, skip=0, limit=100):
    query = select(Director).offset(skip).limit(limit)
    return db.scalars(query).all()


def create_director(db, director_schema):
    director_data = director_schema.model_dump()
    db_director = Director(**director_data)

    db.add(db_director)
    db.commit()
    db.refresh(db_director)
    return db_director


def update_director(db, db_director, director_update):
    update_data = director_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_director, key, value)

    db.commit()
    db.refresh(db_director)
    return db_director


def delete_director(db, db_director):
    db.delete(db_director)
    db.commit()


def get_movies_by_director(db, director_id: int):
    director = get_director(db, director_id)
    return director.movies if director else None
