from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


# Initialize SQLAlchemy without attaching it to any app yet
db = SQLAlchemy()


class User(db.Model, UserMixin):
    """
    users table with id, name, password hash
    and one-to-many relationship to movies
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    # Relationship to Movie
    movies = relationship("Movie", back_populates="user")

    def set_password(self, password):
        """generate password hash"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """check password hash"""
        return check_password_hash(self.password_hash, password)

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
    review = Column(String)

    # Relationship to User
    user = relationship("User", back_populates="movies")

    def __repr__(self):
        """visual representation of movie object"""
        return f"Movie {self.name} ({self.year}): rated {self.rating}"
