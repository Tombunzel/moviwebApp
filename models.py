from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

# Initialize SQLAlchemy without attaching it to any app yet
db = SQLAlchemy()


# Association Table for the many-to-many relationship between Users and Movies
user_movie_favorites = Table(
    'user_movie_favorites',
    db.Model.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('movie_id', Integer, ForeignKey('movies.id'), primary_key=True)
)


class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    # Many-to-Many relationship with Movie
    favorite_movies = relationship("Movie", secondary=user_movie_favorites, back_populates="favorited_by")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"User {self.id}: {self.name}"


class Movie(db.Model):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    director = Column(String)
    year = Column(Integer)
    rating = Column(Float)
    poster_url = Column(String, nullable=True)
    imdb_url = Column(String, nullable=True)

    # Many-to-Many relationship with User
    favorited_by = relationship("User", secondary=user_movie_favorites, back_populates="favorite_movies")

    def __repr__(self):
        return f"Movie {self.name} ({self.year}): rated {self.rating}"
