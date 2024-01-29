from . import Base

from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Boolean,
    DateTime,
)


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    join_date = Column(DateTime)
    last_active = Column(DateTime)
    
    block_date = Column(DateTime, default=None)
    active = Column(Boolean, default=True)
    
    chat_type = Column(String)
    
    ref = Column(String)
    
    def __str__(self):
        return self.id
