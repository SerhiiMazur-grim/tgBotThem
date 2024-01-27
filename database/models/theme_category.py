from . import Base
from .theme_catalog import ThemeInCatalog

from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
)


class ThemeCategory(Base):
    __tablename__ = 'theme_categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique=True)
    themes = relationship('ThemeInCatalog', back_populates='category', cascade='all, delete-orphan')
    active = Column(Boolean, default=True)
    create_date = Column(DateTime)
    
    def __str__(self):
        return self.id
