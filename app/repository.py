import os

from datetime import datetime
from dotenv import load_dotenv  # Импортируем dotenv
from sqlalchemy.exc import IntegrityError
from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, Session, SQLModel, create_engine, select

load_dotenv()  # Загрузка переменных окружения из файла .env


def get_engine():
    database_url = os.getenv("DATABASE_URL")
    return create_engine(database_url, echo=True)

def init_db():
    SQLModel.metadata.create_all(get_engine())


class Links(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    original_url: str
    short_name: str = Field(index=True, unique=True)
    short_url: str
    created_at: datetime | None = Field(
        default=None,
            sa_column=Column(
                DateTime(timezone=True),
                nullable=False,
                server_default=func.now(),
        ),
    )


    @classmethod
    def get_links(cls):
        with Session(get_engine()) as session:
            statement = select(cls)
            results = session.exec(statement)
            links = results.all()
            return [row.model_dump(exclude={"created_at"}) for row in links]

    @classmethod
    def find_link_by_id(cls, id):
        with Session(get_engine()) as session:
            statement = select(cls).where(cls.id == id)
            result = session.exec(statement)
            link = result.first()
            if link:
                return link.model_dump(exclude={"created_at"})
            return None

    @classmethod
    def find_link_by_short_name(cls, short_name):
        with Session(get_engine()) as session:
            statement = select(cls).where(cls.short_name == short_name)
            result = session.exec(statement)
            link = result.first()
            if link:
                return link.model_dump(exclude={"created_at"})
            return None

    @classmethod
    def add_link(cls, original_url, short_name, short_url):
        try:
            with Session(get_engine()) as session:
                link = cls(original_url=original_url, 
                    short_name=short_name, 
                    short_url=short_url)
                session.add(link)
                session.commit()
                session.refresh(link)  # ← обновляем объект (получаем id)
                return link.model_dump(exclude={"created_at"})
        except IntegrityError:
            # short_name уже существует (UNIQUE constraint)
            return None

    @classmethod
    def delete_link(cls, id):
        with Session(get_engine()) as session:
            statement = select(cls).where(cls.id == id)
            link = session.exec(statement).one_or_none()
            if link is None:
                return None
            session.delete(link)
            session.commit()
            return True

    @classmethod
    def update_link(cls, id, original_url, short_name, short_url):
        with Session(get_engine()) as session:
            statement = select(cls).where(cls.id == id)
            link = session.exec(statement).one_or_none()
            if link is None:
                return None
            try:
                link.original_url = original_url
                link.short_name = short_name
                link.short_url = short_url
                session.add(link)
                session.commit()
                session.refresh(link)
                return link.model_dump(exclude={"created_at"})
            except IntegrityError:
                # short_name уже существует (UNIQUE constraint)
                return False
        