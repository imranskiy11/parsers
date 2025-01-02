from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import RUN_TABLE_NAME


Base = declarative_base()


class Review(Base):
    __tablename__ = RUN_TABLE_NAME

    id = Column(Integer, primary_key=True, autoincrement=True)
    author = Column(String(255), nullable=False)
    rating = Column(String(255), nullable=False)
    review_text = Column(Text, nullable=False)
    helpful_count = Column(String(255), nullable=True)
    review_date = Column(String(100), nullable=False)
    dev_reply = Column(Text, nullable=True)


def get_engine(database_url: str):
    return create_engine(database_url)


def create_tables(database_url: str):
    engine = get_engine(database_url)
    Base.metadata.create_all(engine)


def get_session(database_url: str):
    engine = get_engine(database_url)
    Session = sessionmaker(bind=engine)
    return Session()