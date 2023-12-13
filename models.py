from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    """Connect this database to provided Flask app.
    You should call this in your Flask app.
    """
    app.app_context().push()
    db.app = app
    db.init_app(app)

class User(db.Model):
    """
    User.

    Fields:
    - Username (Primary-Key with Foreign-Key relation to notes.owner_username)
    - Password (stores hashed passwords)
    - Email
    - First Name
    - Last Name
    """

    __tablename__ = "users"

    username = db.Column(
        db.String(20),
        primary_key=True
    )
    #Acts as a primary-key to foreign-key of notes.owner_username
    #user = db.relationship('User', backref='notes')

    password = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(50),
        nullable=False,
        unique=True
    )

    first_name = db.Column(
        db.String(30),
        nullable=False
    )

    last_name = db.Column(
        db.String(30),
        nullable=False
    )

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register user with hashed password & return user."""

        hashed = bcrypt.generate_password_hash(password).decode('utf8')

        # return instance of user with hashed pwd
        return cls(
            username=username,
            password=hashed,
            email=email,
            first_name=first_name,
            last_name=last_name
            )

    @classmethod
    def authenticate(cls, username, password):
        """
        Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = cls.query.filter_by(username=username).one_or_none()

        if u and bcrypt.check_password_hash(u.password, password):
            # return user instance
            return u
        else:
            return False

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return f"<User:{self.username}, {self.email}>"




class Note(db.Model):
    """
    Note.

    Fields:
    - id (serialized primary key)
    - title
    - content
    - owner_username (Foreign Key to `users.username`)
    """

    __tablename__ = "notes"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    title = db.Column(
        db.String(100),
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    #redundant string length max
    owner_username = db.Column(
        db.String(20),
        db.ForeignKey('users.username'),
        nullable=False
    )

    user = db.relationship('User', backref='notes')

    def __repr__(self):
        return f"<Note: {self.title} by {self.owner_username}>"


