from . import Base

from sqlalchemy import (
    Column,
    BigInteger,
    Boolean,
    DateTime,
)


class GroupChat(Base):
    __tablename__ = 'group_chats'

    id = Column(BigInteger, primary_key=True)
    
    join_date = Column(DateTime)
    last_active = Column(DateTime)
    
    active = Column(Boolean, default=True)
    
    def __str__(self):
        return self.id
