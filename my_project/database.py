import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

with open('config/app.yml', 'r') as f:
    config = yaml.safe_load(f)['database']
print(f"DEBUG: database.py - Створено URL: ...@{config['db_host']}")

DATABASE_URL = (
    f"mysql+mysqlconnector://"
    f"{config['db_user']}:{config['db_pass']}@"
    f"{config['db_host']}:{config['db_port']}/"
    f"{config['db_name']}"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()