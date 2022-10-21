"""CRUD operations."""
from model import db, User, Movie, Rating, connect_to_db

def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user    

def create_movie(title, overview, release_date, poster_path):
    """Create and return a new movie."""

    movie = Movie(
        title=title,
        overview=overview,
        release_date=release_date,
        poster_path=poster_path,
    )
    
    return movie

def get_movies():
    """Return all movies"""
    return Movie.query.all()

def get_movie_by_id(movie_id):
    """Get movie by movie_id"""
    return Movie.query.get(movie_id)

def create_rating(user, movie, score):
    """Create and return a new rating."""

    rating = Rating(user=user, movie=movie, score=score)

    return rating
    
def get_users():
    """Show user email and link profile"""
    return User.query.all()

def get_user_individual(email):
    return User.query.get(email)

def get_user_by_email(email):
    return User.query.filter(User.email == email).first()

def check_email_and_pass(email, password):
    return User.query.filter(User.password == password).first() and User.query.filter(User.email == email).first()

if __name__ == '__main__':
    from server import app
    connect_to_db(app)