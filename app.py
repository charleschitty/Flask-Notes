"""Flask app for Flask Notes"""

import os

from flask import Flask, render_template, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, User, connect_db
from forms import RegisterForm, LoginForm, LogoutForm

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", "postgresql:///notes")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

debug = DebugToolbarExtension(app)

@app.get("/")
def index():
    """Redirect to /register"""

    return redirect("/register")

@app.route("/register", methods = ["GET","POST"])
def register():
    """
    Shows form that accepts username, password, email, and first and last name,
    and creates a user from that information if the username and email are both
    available. Redirects to user page if successful, re-renders page otherwise.
    """

    form = RegisterForm()

    if form.validate_on_submit():

        if (User.query.filter_by(username=form.username.data).one_or_none()):
            form.username.errors = ["Username already taken"]
        elif (User.query.filter_by(email=form.email.data).one_or_none()):
            form.email.errors = ["An account with that email already exists"]
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

            session["username"] = new_user.username

            return redirect(f"/users/{new_user.username}")

    return render_template("register.html", form=form)


@app.route("/login", methods = ["GET", "POST"])
def login():
    """
    Shows a form that takes in username and password and logs user in with them,
    redirecting to their user page if successful and re-rendering the page
    otherwise.
    """

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username
            return redirect(f"/users/{user.username}")

        else:
            form.username.errors = ["Invalid name/password"]

    return render_template("login.html", form=form)


@app.get("/users/<username>")
def show_user(username):
    """
    Displays the user's non-password information, if logged in.
    Has a button to log out.
    """

    user = User.query.get_or_404(username)
    form = LogoutForm()

    if "username" not in session:
        flash("You must be logged in to view!")
        return redirect("/")
    elif session["username"] != user.username:
        flash(f"Only {user.username} can view this page!")
        return redirect("/")

    return render_template("user.html", user=user, form=form)

@app.post("/logout")
def logout():
    """Log the user out and redirect to '/'"""

    form = LogoutForm()

    if form.validate_on_submit():
        session.pop("username", None)

    return redirect('/')