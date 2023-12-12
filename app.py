"""Flask app for Flask Notes"""

import os

from flask import Flask, jsonify, render_template, flash, redirect
from models import db, User, connect_db

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", "postgresql:///notes")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

@app.get("/")
def index():
    """Redirect to /register"""

    return redirect("/register")

@app.route("/register", methods = ["GET","POST"])
def register():
    """
    Show a form that, when submitted, will register/create a user. This form
    should accept a username, password, email, first_name, and last_name.

    Make sure you are using WTForms and that your password input hides the
    characters that the user is typing.

    Process the registration form by adding a new user. Then redirect to
    /users/<username> (you’ll make this route in the next step)
    """

    #form = our form
    #care for CSRF
    #validate_on_submit
        #check that validation
        #create a user
        #redirect to /users/<username>

    #render html to form again

@app.route("/login", methods = ["GET", "POST"])
def login():
    """
    Show a form that when submitted will login a user. This form should
    accept a username and a password.

    Process the login form, ensuring the user is authenticated and going to
    /users/<username> if so (you’ll make this route in the next step).
    """

    #form = our form
    #care for CSRF
    #validate_on_submit
        #check that validation
        #create a user
        #redirect to /users/<username>

    #render html to form again

@app.get("/users/<username>")
def show_user(username):
    """
    Display a template the shows information about that user (everything
    except for their password)

    Make sure that only the logged-in user can see their page.
    """

    user = User.query.get_or_404(username)

    #if session[user.id] ...

    return render_template(".html", user=user)

@app.post("/logout")
def logout():
    """Log the user out and redirect to '/'"""

    #Form checks CSRF form
    #if validate_on_submit to check if the form is legit (hidden fields)

    return redirect('/')