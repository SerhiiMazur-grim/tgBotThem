from typing import TYPE_CHECKING

from . import Base

from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
    Boolean,
    ForeignKey,
    ARRAY
)


class ChanelOP(Base):
    __tablename__ = 'op'

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    chanel_id = Column(Text)
    invate_url = Column(Text)
    
    join_date = Column(DateTime)
    
    def __str__(self):
        return self.id