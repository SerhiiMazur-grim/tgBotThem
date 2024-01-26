from . import Base

from sqlalchemy import (
    Column, 
    Integer, 
)


class Settings(Base):
    __tablename__ = 'settings'

    Id = Column('id', Integer, primary_key=True)

    Timeout = Column('timeout', Integer, default=0)
    RequestTimeout = Column('request_timeout', Integer, default=0)

    Multiplier = Column('multiplier', Integer, default=1)
