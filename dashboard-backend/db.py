# db.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

username = os.environ.get("DB_USERNAME")
password = os.environ.get("DB_PASSWORD")
host = os.environ.get("DB_HOST")
port = os.environ.get("DB_PORT")

# SQLALCHEMY_DATABASE_URL = f'postgresql://{username}:{password}@{host}:{port}/st'

SQLALCHEMY_DATABASE_URL = 'postgresql://petros:petrosforex@st-database1.cx2qm02isqms.us-east-2.rds.amazonaws.com:5432/st'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
