from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.settings import settings

engine = create_engine(settings.DB_URL)


def get_session():
    with Session(engine) as session:  # pragma: nocover
        yield session
