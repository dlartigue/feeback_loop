from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import Date, Numeric
from sqlalchemy import create_engine
from auth import DB_CONNECTION


Base = declarative_base()


class weight(Base):
    __tablename__ = 'weight'
    date = Column(Date, primary_key=True)
    weight = Column(Numeric, nullable=True)


class energy(Base):
    __tablename__ = 'energy'
    date = Column(Date, primary_key=True)
    calories = Column(Numeric, nullable=True)


if __name__ == '__main__':
    engine = create_engine(DB_CONNECTION)
    Base.metadata.create_all(engine)
