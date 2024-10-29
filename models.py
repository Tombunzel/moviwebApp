from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

# Initialize SQLAlchemy without attaching it to any app yet
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    # Relationship to Movie
    movies = relationship("Movie", back_populates="user")

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
    user_id = Column(Integer, ForeignKey(User.id))

    # Relationship to User
    user = relationship("User", back_populates="movies")

    def __repr__(self):
        return f"Movie {self.name} ({self.year}): rated {self.rating}"
