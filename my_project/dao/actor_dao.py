from sqlalchemy import select
from my_project.domain.models import Actor


def get_actor(db, actor_id: int):
    query = select(Actor).where(Actor.actor_id == actor_id)
    return db.scalars(query).first()


def get_actor_by_name(db, name: str, last_name: str, birth_date: int, nationality: str, bio: str, imdb_code: int):
    query = select(Actor).where(
        Actor.name == name,
        Actor.last_name == last_name,
        Actor.birth_date == birth_date,
        Actor.nationality == nationality,
        Actor.bio == bio,
        Actor.imdb_code == imdb_code
    )
    return db.scalars(query).first()


def get_all_actors(db, skip=0, limit=100):
    query = select(Actor).offset(skip).limit(limit)
    return db.scalars(query).all()


def create_actor(db, actor_schema):
    actor_data = actor_schema.model_dump()
    db_actor = Actor(**actor_data)

    db.add(db_actor)
    db.commit()
    db.refresh(db_actor)
    return db_actor


def update_actor(db, db_actor, actor_update):
    update_data = actor_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_actor, key, value)

    db.commit()
    db.refresh(db_actor)
    return db_actor


def delete_actor(db, db_actor):
    db.delete(db_actor)
    db.commit()


def get_movies_by_actor(db, actor_id: int):
    actor = get_actor(db, actor_id)
    return actor.movies if actor else None
