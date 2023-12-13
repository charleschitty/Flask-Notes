"""Flask app for Flask Notes"""

import os

from flask import Flask, render_template, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, User, connect_db, Note
from forms import RegisterForm, LoginForm, CSRFValidationForm, AddNoteForm, EditNoteForm

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", "postgresql:///notes")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

debug = DebugToolbarExtension(app)

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

USERNAME = "username"

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


@app.post("/logout")
def logout():
    """Log the user out and redirect to '/'"""

    form = CSRFValidationForm()

    if form.validate_on_submit():
        session.pop(USERNAME, None)
    else:
        raise PermissionError("BEGONE")

    return redirect('/')


#*****************************USERS********************************************#


@app.get("/users/<username>")
def show_user(username):
    """
    Displays the user's non-password information, if logged in.
    Has a button to log out.
    """

    form = CSRFValidationForm()

    if USERNAME not in session or session[USERNAME] != username:
        flash(f"You cannot view this page")
        return redirect("/")

    user = User.query.get_or_404(username)

    return render_template("user.html", user=user, form=form)

#not a delete request?? hmm
@app.post("/users/<username>/delete")
def delete_user(username):
    """
    Removes user and their notes from database. Logs user out and
    redirects to /.
    """

    if USERNAME not in session or session[USERNAME] != username:
        flash(f"You cannot view this page")
        return redirect("/")

    user = User.query.get_or_404(username)

    for note in user.notes:
        db.session.delete(note)

    db.session.delete(user)
    db.session.commit()

    session.pop(USERNAME, None)

    return redirect("/")



#*****************************Notes********************************************#


@app.route("/users/<username>/notes/add", methods=["GET","POST"])
def add_note(username):
    """Shows form to add notes that are attached to user once submitted and
    redirects to user's page."""

    if USERNAME not in session or session[USERNAME] != username:
        flash(f"You cannot view this page")
        return redirect("/")

    form = AddNoteForm()

    if form.validate_on_submit():
        new_note = Note(
            title=form.title.data,
            content=form.content.data,
            owner_username=username
            )

        db.session.add(new_note)
        db.session.commit()

        return redirect(f"/users/{username}")
    else:
        return render_template("add_note.html", form=form)

#patch but no?
@app.route("/notes/<int:note_id>/update", methods=["GET","POST"])
def update_note(note_id):
    """Shows form to update a user's notes upon submission and redirects
    to user's page."""

    note = Note.query.get_or_404(note_id)

    if USERNAME not in session or session[USERNAME] != note.owner_username:
        flash(f"You cannot view this page")
        return redirect("/")

    form = EditNoteForm()

    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data

        db.session.add(note)
        db.session.commit()

        return redirect(f"/users/{note.owner_username}")

    else:
        form.title.data = note.title
        form.content.data = note.content
        return render_template("edit_note.html", form=form)


@app.post("/notes/<int:note_id>/delete")
def delete_note(note_id):
    """Deletes a note and redirects to to user's page."""

    note = Note.query.get_or_404(note_id)

    if USERNAME not in session or session[USERNAME] != note.owner_username:
        flash(f"You cannot view this page")
        return redirect("/")

    username = note.owner_username

    form = CSRFValidationForm()

    if form.validate_on_submit():
        db.session.delete(note)
        db.session.commit()

        return redirect(f"/users/{username}")

    else:
        raise PermissionError("STOP")


