
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from my_project.database import Base
import uuid


class Movie(Base):
    __tablename__ = 'movies'

    movie_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(60), nullable=False)
    release_year = Column(Integer, nullable=False)
    director_id = Column(Integer, ForeignKey('directors.director_id', 
                                             ondelete='CASCADE', 
                                             onupdate='CASCADE'))
    director = relationship("Director", back_populates="movies")
    actors = relationship("MovieActor", back_populates="movie", cascade="all, delete-orphan")

class Director(Base):
    __tablename__ = 'directors'

    director_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(45), nullable=False)
    last_name = Column(String(45), nullable=False)
    imdb_code = Column(String(20), nullable=False, unique=True, 
                       default=lambda: str(uuid.uuid4())[:20]) 
    nationality = Column(String(45), nullable=True) 
    movies = relationship("Movie", back_populates="director")

class Actor(Base):
    __tablename__ = 'actors'

    actor_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(45), nullable=False)

    movies = relationship("MovieActor", back_populates="actor", cascade="all, delete-orphan")

class MovieActor(Base):
    __tablename__ = 'movie_actors'

    movie_id = Column(
    Integer,
    ForeignKey('movies.movie_id', ondelete='CASCADE', onupdate='CASCADE'),
    primary_key=True
    )

    actor_id = Column(
        Integer,
        ForeignKey('actors.actor_id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True
    )
    
    movie = relationship("Movie", back_populates="actors")
    actor = relationship("Actor", back_populates="movies")
