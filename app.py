import os
import sqlalchemy
from flask import Flask, render_template, request, flash, redirect, url_for
from sqlalchemy import and_

from datamanager.sqlite_data_manager import SQLiteDataManager
from models import User, Movie, db

app = Flask(__name__)

# Database path
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/moviwebapp.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

# Initialize SQLiteDataManager
data_manager = SQLiteDataManager(app)


@app.route('/')
def home():
    return render_template('home.html'), 200


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users), 200


@app.route('/users/<int:user_id>', methods=['GET'])
def user_movies(user_id):
    movies = data_manager.get_user_movies(user_id)
    return render_template('user_movies.html',
                           movies=movies,
                           user_id=user_id), 200


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        user_name = request.form['name']
        data_manager.add_user(name=user_name)
        flash("User created successfully", "success")
        return redirect(url_for('home')), 201
    else:
        return render_template('add_user.html'), 200


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    if request.method == 'POST':
        name = request.form['name']
        try:
            result = db.session.execute(
                db.select(Movie)
                .where(and_(Movie.name == name,
                            Movie.user_id == user_id))
            ).scalars().one()

        except sqlalchemy.exc.NoResultFound:
            result = False

        if result:
            movie = result
        else:
            movie = Movie(name=name)
            data_manager.add_movie(movie, user_id)
        # data_manager.add_favorite_movie(user_id, movie.id)
        flash("Movie successfully saved to user", "success")
        return redirect(url_for("home"))
    else:
        return render_template('add_movie.html', user_id=user_id), 200


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    movie_to_update = db.session.execute(
        db.select(Movie)
        .where(and_(Movie.id == movie_id,
                    Movie.user_id == user_id))
    ).scalars().one()

    if not movie_to_update:
        flash("Couldn't find movie in the database")
        return redirect(url_for('home'))

    if request.method == 'POST':
        new_info = {
            'name': request.form['name'],
            'director': request.form['director'],
            'rating': request.form['rating'],
            'year': request.form['year']
        }
        data_manager.update_movie(movie_to_update, new_info)
        flash("Movie successfully updated", "success")
        return redirect(url_for('home'))

    else:
        return render_template('update_movie.html', movie=movie_to_update)


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['GET'])
def delete_movie(user_id, movie_id):
    movie = db.session.execute(
        db.select(Movie)
        .where(Movie.id == movie_id)
    ).scalars().one()
    user = db.session.execute(
        db.select(User)
        .where(User.id == user_id)
    ).scalars().one()

    if not user or not movie:
        raise ValueError("User or Movie not found")

    if movie in user.favorite_movies:
        user.favorite_movies.remove(movie)
        db.session.commit()
        flash("Movie successfully removed from user's favorites", "success")
        return redirect(url_for('home')), 204
    else:
        flash("Movie is not in user's favorites", "danger")
        return redirect(url_for('home')), 404


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', error=e), 404


if __name__ == '__main__':
    with app.app_context():
        # db.drop_all()  # Drops all tables
        db.create_all()  # Recreates them with the latest schema

    app.run(host="0.0.0.0", port=5000, debug=True)
