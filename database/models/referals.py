from . import Base

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
)


class Referal(Base):
    __tablename__ = 'referals'

    id = Column(Integer, primary_key=True, autoincrement=True)
            
    ref = Column(String, unique=True)
    
    total_users = Column(Integer)
    active_users = Column(Integer)
    
    join_date = Column(DateTime)
    
    def __str__(self):
        return self.id
