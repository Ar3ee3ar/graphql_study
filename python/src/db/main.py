import os
from dotenv import load_dotenv
from sqlmodel import create_engine, SQLModel, Session
from typing import Annotated
from fastapi import Depends

load_dotenv()

db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{db_username}:{db_password}@{db_host}/{db_name}"
engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session