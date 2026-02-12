from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session

_sqlite_file_name = "database.db"
_sqlite_url = f"sqlite:///{_sqlite_file_name}"

_connect_args = {"check_same_thread": False}
_engine = create_engine(_sqlite_url, connect_args=_connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(_engine)


def _get_session():
    with Session(_engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(_get_session)]