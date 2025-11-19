
from pydantic import BaseModel
from typing import Optional
from datetime import date

class MovieBase(BaseModel):
    title: str
    release_year: int
    director_id: int   

class MovieCreate(MovieBase):
    pass

class MovieUpdate(BaseModel):
    title: Optional[str] = None
    release_year: Optional[int] = None
    director_id: Optional[int] = None

class MovieResponse(MovieBase):
    movie_id: int

    class Config:
        from_attributes = True


class DirectorBase(BaseModel):
    first_name: str
    last_name: str
    imdb_code: str
    nationality: str

class DirectorCreate(DirectorBase):
    pass

class DirectorUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    imdb_code: Optional[str] = None
    nationality: Optional[str] = None

class DirectorResponse(DirectorBase):
    director_id: int
    first_name: str
    last_name: str
    imdb_code: str
    nationality: str | None = None

    class Config:
        from_attributes = True

class ActorBase(BaseModel):
    name: str

class ActorCreate(ActorBase):
    pass

class ActorUpdate(BaseModel):
    name: Optional[str] = None

class ActorResponse(ActorBase):
    actor_id: int

    class Config:
        from_attributes = True


class MovieActorBase(BaseModel):
    movie_id: int
    actor_id: int

class MovieActorResponse(MovieActorBase):
    class Config:
        from_attributes = True
