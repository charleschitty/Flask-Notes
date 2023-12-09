"""Flask app for Flask Notes"""

import os

from flask import Flask, jsonify, render_template, flash, redirect
from models import db, User, connect_db
from forms import RegisterForm, LoginForm, LogoutForm

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

    form = RegisterForm()

    if form.validate_on_submit():

        if (User.query.one_or_none(form.username.data)):
            form.username.errors["Username already taken"]
        else:
            new_user = User.register(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data
            )

            db.session.add(new_user)
            db.session.commit()

        #TODO: Log them in
        flash(f"User {new_user.username} created!")
        return redirect(f"/users/{new_user.username}")
    else:
        return render_template("register.html")

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