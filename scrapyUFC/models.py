from sqlalchemy import create_engine, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String 
from scrapy.utils.project import get_project_settings
from typing import List, Optional


Base = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.  
    Returns sqlalchemy engine instance
    """
    return create_engine(get_project_settings().get("CONNECTION_STRING"))


def create_table(engine):
    Base.metadata.create_all(engine)


class Fighter(Base):
    __tablename__= "fighters"

    id: Mapped[int] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String) 
    nationality: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    locality: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    weight_class: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    wins: Mapped[int] = mapped_column(Integer)
    wins_by_ko_tko: Mapped[int] = mapped_column(Integer)
    wins_by_sub: Mapped[int] = mapped_column(Integer)
    wins_by_dec: Mapped[int] = mapped_column(Integer)
    losses: Mapped[int] = mapped_column(Integer)
    losses_by_ko_tko: Mapped[int] = mapped_column(Integer)
    losses_by_sub: Mapped[int] = mapped_column(Integer)
    losses_by_dec: Mapped[int] = mapped_column(Integer)


class Fight(Base):
    __tablename__ = "fights"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    left_fighter_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    left_status: Mapped[str] = mapped_column(String)
    right_fighter_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    right_status: Mapped[str] = mapped_column(String)
    weight_class: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    method: Mapped[str] = mapped_column(String)
    round: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    time: Mapped[str] = mapped_column(String)
    

class Event(Base):
    __tablename__ = "events"

    title: Mapped[str] = mapped_column(String, primary_key=True)
    date: Mapped[str] = mapped_column(String)
    location: Mapped[str] = mapped_column(String)