from typing import TYPE_CHECKING

from . import Base

from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
)

if TYPE_CHECKING:
    from .language_catalog import LanguageInCatalog


class LanguageCategory(Base):
    __tablename__ = 'languages_categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique=True)
    languages = relationship('LanguageInCatalog', back_populates='category', cascade='all, delete-orphan')
    active = Column(Boolean, default=True)
    create_date = Column(DateTime)
    
    def __str__(self):
        return self.id
