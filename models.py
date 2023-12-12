from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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
    - Username (Primary-Key)
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

    def __repr__(self):
        return f"<User:{self.username}, {self.email}>"


class Note(db.Model):

    __tablename__ = "notes"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    title = db.Column(
        db.Sting(100),
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    owner_username = db.Column(
        db.String(20),
        db.ForeignKey('users.username'),
        nullable=False
    )

    # def __repr__(self):
    #     return f"<PlaylistSong: pID={self.playlist_id}, sID={self.song_id}>"

    # songs = db.relationship('Song', secondary='playlists_songs',
    #                                  backref='playlists')

