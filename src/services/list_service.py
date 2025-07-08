"""
This module defines the ListService class responsible for managing
movie download entries in the database using SQLAlchemy.

It provides methods to add, retrieve, list, update, and delete movie items.
"""

from sqlalchemy.orm import Session
from src.models.list_model import ListModel

class ListService:
    def __init__(self, session: Session):
        """
        Initializes the service with the given SQLAlchemy session.

        Args:
            session (Session): SQLAlchemy session object used to interact with the database.
        """
        self.session = session

    def add_item(self, title: str, link: str) -> ListModel:
        """
        Adds a new movie entry to the database.

        Args:
            title (str): Title of the movie.
            link (str): Download link for the movie.

        Returns:
            ListModel: The created ListModel object with all fields populated.
        """
        item = ListModel(title=title, link=link)
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def get_item(self, item_id: int) -> ListModel | None:
        """
        Retrieves a movie entry by its ID.

        Args:
            item_id (int): ID of the movie entry.

        Returns:
            ListModel | None: The corresponding ListModel object if found, otherwise None.
        """
        return self.session.query(ListModel).get(item_id)

    def list_all(self) -> list[ListModel]:
        """
        Returns a list of all movie entries.

        Returns:
            list[ListModel]: A list of all movie entries in the database.
        """
        return self.session.query(ListModel).all()

    def list_pending(self) -> list[ListModel]:
        """
        Returns a list of movies that have not been downloaded yet.

        Returns:
            list[ListModel]: A list of pending movie entries.
        """
        return self.session.query(ListModel).filter_by(downloaded=False).all()

    def mark_downloaded(self, item_id: int) -> bool:
        """
        Marks a movie entry as downloaded.

        Args:
            item_id (int): ID of the movie entry.

        Returns:
            bool: True if the update was successful, False if the item does not exist.
        """
        item = self.get_item(item_id)
        if not item:
            return False
        item.downloaded = True
        self.session.commit()
        return True

    def delete_item(self, item_id: int) -> bool:
        """
        Deletes a movie entry from the database.

        Args:
            item_id (int): ID of the movie entry to delete.

        Returns:
            bool: True if the deletion was successful, False if the item does not exist.
        """
        item = self.get_item(item_id)
        if not item:
            return False
        self.session.delete(item)
        self.session.commit()
        return True
