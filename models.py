from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

# Initialize SQLAlchemy without attaching it to any app yet
db = SQLAlchemy()


class User(db.Model):
    """
    users table including id and name
    and a one-to-many relationship with movies
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

    # Relationship to Movie
    movies = relationship("Movie", back_populates="user")

    def __repr__(self):
        """visual representation of a user object"""
        return f"User {self.id}: {self.name}"


class Movie(db.Model):
    """movies table with id, name, director, publishing year,
    imdb rating, poster url, country flag icon url, imdb url,
    corresponding user id, and relationship to users
    """
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    director = Column(String)
    year = Column(Integer)
    rating = Column(Float)
    poster_url = Column(String, nullable=True)
    flag_url = Column(String, nullable=True)
    imdb_url = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey(User.id))

    # Relationship to User
    user = relationship("User", back_populates="movies")

    def __repr__(self):
        """visual representation of movie object"""
        return f"Movie {self.name} ({self.year}): rated {self.rating}"
