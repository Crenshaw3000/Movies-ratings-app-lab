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

@app.route('/movies/<movie_id>/rate', methods=["POST"])
def show_rating(movie_id):
    """Show new movie ratings"""

    signed_in_email=session.get("user_email")
    score = request.form.get('score')

    if signed_in_email is None:
        flash(f"You must be signed in!")
    elif not score:
        flash("You didn't select a score")
    else: 
        user = crud.get_user_by_email(signed_in_email)
        movie = crud.get_movie_by_id(movie_id)

        rating = crud.create_rating(user, movie, int(score))
        db.session.add(rating)
        db.session.commit()
        flash(f"You rated this movie {rating.score} out of 5")

    return redirect(f'/movies/{movie_id}')
        

@app.route('/users')
def show_users():

    users = crud.get_users()

    return render_template("all_users.html", users=users)

@app.route('/users', methods=['POST'])
def register_user():
    """Create new user account"""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)

    if user:
        flash("An account with this email already exists.")
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created successfully. Please log in.")
    
    return redirect("/")

@app.route('/login', methods=['POST'])
def login_user():
    """Login to user account"""

    email = request.form.get("email")
    password = request.form.get("password")

    match = crud.check_email_and_pass(email, password)

    if not match:
        flash("This email is not correct. Check again.")
    else:
        session["user_email"]=match.email
        flash("Logged in!")
    
    return redirect("/")


@app.route('/users/<email>')
def show_user_details(email):

    user = crud.get_user_individual(email)
    ratings = user.ratings

    return render_template("user_details.html", user=user, ratings=ratings)

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
