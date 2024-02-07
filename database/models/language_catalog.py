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

if TYPE_CHECKING:
    from .language_category import LanguageCategory


class LanguageInCatalog(Base):
    __tablename__ = 'languages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    preview = Column(Text)
    text = Column(Text)
    
    android = Column(Boolean)
    computer = Column(Boolean)
    ios = Column(Boolean)
    
    category_id = Column(Integer, ForeignKey('languages_categories.id'))
    category = relationship('LanguageCategory', back_populates='languages')
    
    join_date = Column(DateTime)
    
    def __str__(self):
        return self.id
