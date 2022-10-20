"""Server for movie ratings app."""
from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined




@app.route('/')
def homepage():
    """"Return render template to homepage.html"""

    return render_template('homepage.html')

@app.route('/movies')
def all_movies():
    """View all movies"""

    movies = crud.get_movies()

    return render_template("all_movies.html", movies=movies)

@app.route('/movies/<movie_id>')
def show_movie_details(movie_id):
    """Show movie details"""

    movie = crud.get_movie_by_id(movie_id)

    return render_template("movie_details.html", movie=movie)

@app.route('/users')
def show_users():

    users = crud.get_users()

    return render_template("all_users.html", users=users)

@app.route('/users/<email>')
def show_user_details(email):

    
    user = crud.get_user_by_email(email)
    
    return render_template("user_details.html", user=user)

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
