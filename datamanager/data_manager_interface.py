from abc import ABC, abstractmethod


class DataManagerInterface(ABC):
    """this class serves as the large interface
    of the different data manager classes"""
    @abstractmethod
    def get_all_users(self):
        """this function will be implemented by each data manager"""

    @abstractmethod
    def get_user_movies(self, user_id):
        """this function will be implemented by each data manager"""

    @abstractmethod
    def add_user(self, name):
        """this function will be implemented by each data manager"""

    @abstractmethod
    def add_movie(self, movie, user_id):
        """this function will be implemented by each data manager"""

    @abstractmethod
    def update_movie(self, movie, info):
        """this function will be implemented by each data manager"""

    @abstractmethod
    def delete_movie(self, movie_id):
        """this function will be implemented by each data manager"""

    @abstractmethod
    def add_review(self, movie, review):
        """this function will be implemented by each data manager"""
