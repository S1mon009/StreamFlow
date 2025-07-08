"""
This module defines the ListModel class, representing a movie entry
to be downloaded and stored in the database.
"""

from sqlalchemy import Column, Integer, String, Boolean
from src.models.base import Base

class ListModel(Base):
    """
    ORM model for the 'list_model' table.

    Stores information about movies to download, including title,
    download link, and whether they have already been downloaded.
    """
    __tablename__ = 'list_model'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    link = Column(String, nullable=False)
    downloaded = Column(Boolean, default=False, nullable=False)

    def __repr__(self) -> str:
        """
        Returns a string representation of the ListModel instance.

        Returns:
            str: A formatted string containing the id, title, and download status.
        """
        return f"<ListModel(id={self.id}, title='{self.title}', downloaded={self.downloaded})>"
