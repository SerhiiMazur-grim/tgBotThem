from . import Base

from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)


class ThemeInCatalog(Base):
    __tablename__ = 'themes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    preview = Column(String)
    file = Column(String)
    category_id = Column(Integer, ForeignKey('theme_categories.id'))
    category = relationship('ThemeCategory', back_populates='themes')
    join_date = Column(DateTime)
    
    def __str__(self):
        return self.id
