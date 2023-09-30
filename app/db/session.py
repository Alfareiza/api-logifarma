from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.settings import Settings

engine = create_engine(Settings().DB_URL)


def get_session():
    with Session(engine) as session:  # pragma: nocover
        yield session
