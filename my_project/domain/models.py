
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DECIMAL, Date
from sqlalchemy.orm import relationship
from my_project.database import Base


class Movie(Base):
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(60), nullable=False)
    release_year = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    imdb_code = Column(String(30), nullable=False, unique=True)
    rating = Column(DECIMAL(3, 1), nullable=True)

    movie_facts = relationship("MovieFact", back_populates="movie")

    movie_actors = relationship("MovieActor", back_populates="movie")
    actors = relationship("Actor", secondary="movie_actors", back_populates="movies")

    movie_directors = relationship("MovieDirector", back_populates="movie")
    directors = relationship("Director", secondary="movie_directors", back_populates="movies")

class Director(Base):
    __tablename__ = "directors"

    director_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    nationality = Column(String(100), nullable=True)
    imdb_code = Column(String(100), nullable=False)

    movie_directors = relationship("MovieDirector", back_populates="director")
    movies = relationship("Movie", secondary="movie_directors", back_populates="directors")

class Actor(Base):
    __tablename__ = "actors"

    actor_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    birth_date = Column(Date, nullable=True)
    nationality = Column(String(100), nullable=True)
    bio = Column(Text, nullable=True)
    imdb_code = Column(String, nullable=False)
    last_name = Column(Integer, nullable=False)

    movie_actors = relationship("MovieActor", back_populates="actor")
    movies = relationship("Movie", secondary="movie_actors", back_populates="actors")


class MovieActor(Base):
    __tablename__ = "movie_actors"

    movie_id = Column(Integer, ForeignKey("movies.movie_id"), primary_key=True)
    actor_id = Column(Integer, ForeignKey("actors.actor_id"), primary_key=True)
    character_name = Column(String(100), nullable=True)
    billing_order = Column(Integer, nullable=True)

    movie = relationship("Movie", back_populates="movie_actors")
    actor = relationship("Actor", back_populates="movie_actors")

class MovieDirector(Base):
    __tablename__ = "movie_directors"

    movie_id = Column(Integer, ForeignKey("movies.movie_id"), primary_key=True)
    director_id = Column(Integer, ForeignKey("directors.director_id"), primary_key=True)

    movie = relationship("Movie", back_populates="movie_directors")
    director = relationship("Director", back_populates="movie_directors")

# У файлі, де визначено клас MovieFact (наприклад, my_project/domain/models.py або movie_fact.py)

from sqlalchemy import Column, Integer, ForeignKey, Text, String
from sqlalchemy.orm import relationship

class MovieFact(Base):
    __tablename__ = "movie_facts"

    fact_id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(Integer, ForeignKey("movies.movie_id"), nullable=False)
    fact_text = Column(Text, nullable=False)
    source = Column(String(60), nullable=True)

    movie = relationship("Movie", back_populates="movie_facts")