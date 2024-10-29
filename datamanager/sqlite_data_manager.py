from models import db, User, Movie
from datamanager.data_manager_interface import DataManagerInterface
from datamanager.api_fetcher import fetch_api_movie_dict


class SQLiteDataManager(DataManagerInterface):
    """
    SQL data manager class for all manipulations of the database.
    """
    def __init__(self, app):
        """Initialize db with the app
        create tables if they don't exist"""
        self.db = db
        self.db.init_app(app)
        with app.app_context():
            self.db.create_all()

    def user_exists(self, user_id):
        user_exists = self.db.session.execute(self.db.select(User).where(User.id == user_id)).scalar_one_or_none()
        if user_exists:
            return True
        return False

    def movie_exists(self, movie_id):
        movie_exists = self.db.session.execute(self.db.select(Movie).where(Movie.id == movie_id)).scalar_one_or_none()
        if movie_exists:
            return True
        return False

    def get_all_users(self):
        """returns all users in database"""
        return self.db.session.execute(self.db.select(User)).scalars().all()

    def get_all_movies(self):
        """returns all movies in database"""
        return self.db.session.execute(self.db.select(Movie)).scalars().all()

    def get_user_movies(self, user_id):
        """returns all movies of certain user"""
        return self.db.session.execute(
            self.db.select(Movie).where(Movie.user_id == user_id)
        ).scalars().all()

    def add_user(self, name):
        """adds a user to the database"""
        new_user = User(name)
        self.db.session.add(new_user)
        self.db.session.commit()

    def add_movie(self, movie, user_id):
        """
        This function fetches information about a movie from its name,
        then assigns that information to the movie object.
        The movie is then added to the session and the addition commited.
        """
        omdb_dict = fetch_api_movie_dict(movie.name)
        movie.rating = float(omdb_dict['Ratings'][0]['Value'].split('/')[0])
        movie.poster_url = omdb_dict['Poster']
        movie.imdb_url = f"https://www.imdb.com/title/{omdb_dict['imdbID']}"
        movie.director = omdb_dict['Director']
        movie.year = omdb_dict['Year']
        movie.user_id = user_id
        # country = omdb_dict['Country'].split(',')[0]
        # movie.flag_url = fetch_country_flag_url(str(country))
        self.db.session.add(movie)
        self.db.session.commit()

    def update_movie(self, movie, info):
        """
        this function receives a movie (obj) and its info (dict)
        finds the movie in the database and updates it with new info.
        """
        update_fields = {k: v for k, v in info.items() if v is not None}
        if update_fields:
            self.db.session.execute(
                self.db.update(Movie).where(Movie.id == movie.id).values(**update_fields)
            )
            self.db.session.commit()

    def delete_movie(self, movie_id):
        """
        this function deletes a movie from the database
        according to movie_id
        """
        self.db.session.execute(
            self.db.delete(Movie).where(Movie.id == movie_id)
        )
        self.db.session.commit()
