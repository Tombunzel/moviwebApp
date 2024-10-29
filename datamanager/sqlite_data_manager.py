from models import db, User, Movie
from datamanager.data_manager_interface import DataManagerInterface
from datamanager.api_fetcher import fetch_api_movie_dict, fetch_country_flag_url


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, app):
        self.db = db
        # Initialize db with the app
        self.db.init_app(app)
        with app.app_context():
            # Create tables if they don't exist
            self.db.create_all()

    def add_favorite_movie(self, user_id, movie_id):
        user = self.db.session.execute(
            db.select(User)
            .where(User.id == user_id)
        ).scalars().one()
        movie = self.db.session.execute(
            db.select(Movie)
            .where(Movie.id == movie_id)
        ).scalars().one()

        if not user or not movie:
            raise ValueError("User or Movie not found")

        # Add movie to user's favorites if it's not already in the list
        if movie not in user.favorite_movies:
            user.favorite_movies.append(movie)
            self.db.session.commit()
        else:
            print("Movie already favorited by this user")

    def get_user_favorites(self, user_id):
        user = self.db.session.get(User, user_id)
        if not user:
            raise ValueError("User not found")

        return user.favorite_movies  # Returns a list of movies favorited by the user

    def get_movie_favorited_by(self, movie_id):
        movie = self.db.session.get(Movie, movie_id)
        if not movie:
            raise ValueError("Movie not found")

        return movie.favorited_by  # Returns a list of users who favorited this movie

    def get_all_users(self):
        return self.db.session.execute(self.db.select(User)).scalars().all()

    def get_all_movies(self):
        return self.db.session.execute(self.db.select(Movie)).scalars().all()

    def get_user_movies(self, user_id):
        return self.db.session.execute(
            self.db.select(Movie).where(Movie.user_favourite == user_id)
        ).scalars().all()

    def add_user(self, name):
        new_user = User(name)
        self.db.session.add(new_user)
        self.db.session.commit()

    def add_movie(self, movie, user_id):
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
        update_fields = {k: v for k, v in info.items() if v is not None}
        if update_fields:
            self.db.session.execute(
                self.db.update(Movie).where(Movie.id == movie.id).values(**update_fields)
            )
            self.db.session.commit()

    def delete_movie(self, movie_id):
        self.db.session.execute(
            self.db.delete(Movie).where(Movie.id == movie_id)
        )
        self.db.session.commit()

# print(fetch_api_movie_dict("The Green Mile"))
