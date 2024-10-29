from abc import ABC, abstractmethod


class DataManagerInterface(ABC):
    """this class serves as the large interface
    of the different data manager classes"""
    @abstractmethod
    def get_all_users(self):
        """this function will be implemented by each data manager"""
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        """this function will be implemented by each data manager"""
        pass

    @abstractmethod
    def add_user(self, user):
        """this function will be implemented by each data manager"""
        pass

    @abstractmethod
    def add_movie(self, movie, user_id):
        """this function will be implemented by each data manager"""
        pass

    @abstractmethod
    def update_movie(self, movie, info):
        """this function will be implemented by each data manager"""
        pass

    @abstractmethod
    def delete_movie(self, movie):
        """this function will be implemented by each data manager"""
        pass
