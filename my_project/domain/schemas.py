from pydantic import BaseModel
from typing import Optional, List
from datetime import date


class DirectorBase(BaseModel):
    first_name: str
    last_name: str
    imdb_code: str
    nationality: Optional[str] = None

class DirectorCreate(DirectorBase):
    pass

class DirectorUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    imdb_code: Optional[str] = None
    nationality: Optional[str] = None

class DirectorResponse(DirectorBase):
    director_id: int

    class Config:
        from_attributes = True

class ActorBase(BaseModel):
    name: str
    last_name: str
    birth_date: Optional[date] = None
    nationality: Optional[str] = None
    bio: Optional[str] = None
    imdb_code: str

class ActorCreate(ActorBase):
    pass

class ActorUpdate(BaseModel):
    name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[date] = None
    nationality: Optional[str] = None
    bio: Optional[str] = None
    imdb_code: Optional[str] = None

class ActorResponse(ActorBase):
    actor_id: int

    class Config:
        from_attributes = True

class MovieBase(BaseModel):
    title: str
    release_year: int
    duration: int
    description: Optional[str] = None
    imdb_code: str
    rating: Optional[float] = None
class MovieCreate(MovieBase):
    pass

class MovieUpdate(BaseModel):
    title: Optional[str] = None
    release_year: Optional[int] = None
    duration: Optional[int] = None
    description: Optional[str] = None
    imdb_code: Optional[str] = None
    rating: Optional[float] = None

class MovieResponse(MovieBase):
    movie_id: int
    directors_url: str

    class Config:
        from_attributes = True


class MovieActorBase(BaseModel):
    movie_id: int
    actor_id: int
    character_name: Optional[str] = None
    billing_order: Optional[int] = None

class MovieActorResponse(MovieActorBase):
    class Config:
        from_attributes = True


class MovieDirectorBase(BaseModel):
    movie_id: int
    director_id: int

class MovieDirectorResponse(MovieDirectorBase):
    class Config:
        from_attributes = True


class MovieFactBase(BaseModel):
    # movie_id: int
    fact_text: str
    # source: Optional[str] = None

class MovieFactCreate(MovieFactBase):
    pass

class MovieFactUpdate(BaseModel):
    fact_text: Optional[str] = None
    source: Optional[str] = None

class MovieFactResponse(MovieFactBase):
    # fact_id: int
    fact_text: str
    # source: Optional[str] = None

    class Config:
        from_attributes = True


class MovieResponse(MovieBase):
    pass

    class Config:
        from_attributes = True

class MovieWithFactsResponse(MovieResponse): 
    movie_facts: List[MovieFactResponse] 

    class Config:
        from_attributes = True