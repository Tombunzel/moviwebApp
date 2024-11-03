import os
import sqlalchemy
from flask import Flask, render_template, request, flash, redirect, url_for
from sqlalchemy import and_
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datamanager import openai_api
from datamanager.sqlite_data_manager import SQLiteDataManager
from models import User, Movie, db

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database path
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/moviwebapp.sqlite')
# App configurations
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
# Initialize SQLiteDataManager
data_manager = SQLiteDataManager(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = db.session.execute(
            db.select(User).where(User.name == request.form['username'])
        ).scalar_one_or_none()

        if user and user.check_password(request.form['password']):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('home'))
        flash('Invalid username or password')
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/')
def home():
    """home page route"""
    movies = data_manager.get_all_movies()
    return render_template('home.html', movies=movies), 200


@app.route('/users')
def list_users():
    """route that displays all the available users"""
    users = data_manager.get_all_users()
    return render_template('users.html', users=users), 200


@app.route('/users/<int:user_id>', methods=['GET'])
@login_required
def user_movies(user_id):
    user_exists = data_manager.user_exists(user_id)
    if user_exists:
        # Authorisation check
        if current_user.id != user_id:
            flash("You don't have permission to view this page")
            return redirect(url_for('home'))
        movies = data_manager.get_user_movies(user_id)
        return render_template('user_movies.html',
                               movies=movies,
                               user_id=user_id), 200

    message = "Couldn't find user in the database"
    return render_template('404.html', error=message), 404


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        user_name = request.form['name']
        password = request.form['password']
        try:
            new_user = User(name=user_name)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            flash("That user name is already taken", "danger")
            return redirect(url_for('add_user'))

        flash("User created successfully", "success")
        return redirect(url_for('login'))

    return render_template('add_user.html'), 200


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
@login_required
def add_movie(user_id):
    """route that adds a movie to a certain user"""
    user_exists = data_manager.user_exists(user_id)
    if not user_exists:
        message = "Couldn't find user in the database"
        return render_template('404.html', error=message)

    # Authorisation check
    if current_user.id != user_id:
        flash("You don't have permission to view this page")
        return redirect(url_for('home'))

    if request.method == 'POST':
        name = request.form['name']
        movie = Movie(name=name)
        error = data_manager.add_movie(movie, user_id)
        if error:
            message = error
            return render_template('404.html', error=message)
        flash("Movie successfully saved to user", "success")
        return redirect(url_for("user_movies", user_id=user_id))
    return render_template('add_movie.html', user_id=user_id)


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def update_movie(user_id, movie_id):
    """route that allows the user to update movie information"""
    # Authorisation check
    if current_user.id != user_id:
        flash("You don't have permission to view this page")
        return redirect(url_for('home'))

    movie_to_update = db.session.execute(
        db.select(Movie)
        .where(and_(Movie.id == movie_id,
                    Movie.user_id == user_id))
    ).scalars().one()

    if not movie_to_update:
        flash("Couldn't find movie in the database")
        return redirect(url_for('user_movies', user_id=user_id))

    if request.method == 'POST':
        new_info = {
            'name': request.form['name'],
            'director': request.form['director'],
            'rating': request.form['rating'],
            'year': request.form['year'],
            'review': request.form['review']
        }
        data_manager.update_movie(movie_to_update, new_info)
        flash("Movie successfully updated", "success")
        return redirect(url_for('user_movies', user_id=user_id))
    return render_template('update_movie.html', movie=movie_to_update)


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['POST'])
@login_required
def delete_movie(user_id, movie_id):
    """route to delete a movie from user favorites"""
    # Authorisation check
    if current_user.id != user_id:
        flash("You don't have permission to view this page")
        return redirect(url_for('home'))

    movie = db.session.execute(
        db.select(Movie)
        .where(and_(Movie.id == movie_id,
                    Movie.user_id == user_id))
    ).scalar_one_or_none()

    if not movie:
        message = "Couldn't find movie in database"
        return render_template('404.html', error=message), 404

    db.session.delete(movie)
    db.session.commit()
    flash("Movie successfully removed from user's favorites", "success")
    return redirect(url_for('user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/delete_user', methods=['GET'])
@login_required
def delete_user(user_id):
    """delete user and its movies from the database"""
    # Authorisation check
    if current_user.id != user_id:
        flash("You don't have permission to view this page")
        return redirect(url_for('home'))

    user = db.session.execute(db.select(User).where(User.id == user_id)).scalars().one()
    movies = db.session.execute(db.select(Movie).where(Movie.user_id == user_id)).scalars().all()
    db.session.delete(user)
    for movie in movies:
        db.session.delete(movie)
    db.session.commit()
    flash("User successfully deleted", "success")
    return redirect(url_for('list_users'))


@app.route('/users/<int:user_id>/add_review/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def add_review(user_id, movie_id):
    """
    route to add a user review to a movie
    if the user clicks on 'generate review', openai_api will generate a review
    and insert it into the template
    """
    # Authorisation check
    if current_user.id != user_id:
        flash("You don't have permission to view this page")
        return redirect(url_for('home'))

    movie = db.session.execute(
        db.select(Movie)
        .where(and_(Movie.id == movie_id,
                    Movie.user_id == user_id))
    ).scalar_one_or_none()

    if not movie:
        flash("Couldn't find movie in the database")
        return redirect(url_for('user_movies', user_id=user_id))

    if request.method == 'POST':
        try:
            generate = request.form['generate']
            response = openai_api.generate_review(movie.name)
            if response.status_code == 429:
                flash("Too many requests, couldn't generate a review", "danger")
                return redirect(url_for('user_movies', user_id=user_id))
            elif response.status_code == 200:
                review = response.json()['result']
                return render_template('add_review.html', movie=movie, review=review)
            else:
                flash("Sorry, couldn't generate a review", "danger")
                return redirect(url_for('user_movies', user_id=user_id))
        except KeyError:
            pass

        review = request.form['review']
        data_manager.add_review(movie, review)
        flash("Review successfully added", "success")
        return redirect(url_for('user_movies', user_id=user_id))

    return render_template('add_review.html', movie=movie)


@app.route('/users/<int:user_id>/show_review/<int:movie_id>', methods=['GET'])
@login_required
def show_review(user_id, movie_id):
    """route to show a movie's user review"""
    # Authorisation check
    if current_user.id != user_id:
        flash("You don't have permission to view this page")
        return redirect(url_for('home'))

    movie = db.session.execute(
        db.select(Movie)
        .where(and_(Movie.id == movie_id,
                    Movie.user_id == user_id))
    ).scalar_one_or_none()
    return render_template('show_review.html', movie=movie)


@app.route('/users/<int:user_id>/recommendation', methods=['GET'])
@login_required
def get_recommendation(user_id):
    """
    based on the movies saved to a user, openai_api will recommend a new movie
    """
    # Authorisation check
    if current_user.id != user_id:
        flash("You don't have permission to view this page")
        return redirect(url_for('home'))

    movies = db.session.execute(db.select(Movie).where(Movie.user_id == user_id)).scalars().all()
    response = openai_api.generate_recommendation(movies)
    if response.status_code == 429:
        flash("Too many requests, couldn't generate a recommendation", "danger")
        return redirect(url_for('user_movies', user_id=user_id))
    elif response.status_code == 429:
        recommendation = response.json()['result']
        return render_template('recommendation.html', recommendation=recommendation, user_id=user_id)
    else:
        flash("Sorry, couldn't generate a recommendation", "danger")
        return redirect(url_for('user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/trivia/<int:movie_id>')
@login_required
def get_trivia(user_id, movie_id):
    """
    based on movie and user ID, this function uses
    openai_api to generate a trivia about the movie
    """
    # Authorisation check
    if current_user.id != user_id:
        flash("You don't have permission to view this page")
        return redirect(url_for('home'))

    movie = db.session.execute(
        db.select(Movie)
        .where(and_(Movie.id == movie_id,
                    Movie.user_id == user_id))
    ).scalar_one_or_none()

    if not movie:
        return {"trivia": "Movie not found"}, 404

    trivia = openai_api.generate_trivia(movie.name)
    return {"trivia": trivia}, 200


@app.errorhandler(404)
def page_not_found(e):
    """error handler for 404 status codes"""
    return render_template('404.html', error=e), 404


if __name__ == '__main__':
    # with app.app_context():
    #     db.drop_all()  # Drops all tables
    #     db.create_all()  # Recreates them with the latest schema

    app.run(host="0.0.0.0", port=5000, debug=True)
