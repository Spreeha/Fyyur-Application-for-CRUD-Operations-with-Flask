from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#
from flask import Flask
from flask_moment import Moment
app = Flask(__name__)
moment = Moment(app)
app.config.from_object("config")
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Genre(db.Model):
    __tablename__ = "Genre"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


artist_genre_table = db.Table(
    "artist_genre_table",
    db.Column("genre_id", db.Integer, db.ForeignKey("Genre.id"), primary_key=True),
    db.Column("artist_id", db.Integer, db.ForeignKey("Artist.id"), primary_key=True),
)

venue_genre_table = db.Table(
    "venue_genre_table",
    db.Column("genre_id", db.Integer, db.ForeignKey("Genre.id"), primary_key=True),
    db.Column("venue_id", db.Integer, db.ForeignKey("Venue.id"), primary_key=True),
)


class Venue(db.Model):
    __tablename__ = "Venue"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(120))

    # many to many relationship between Venue and Genre with Venue being the parent table
    genres = db.relationship(
        "Genre", secondary=venue_genre_table, backref=db.backref("venues")
    )

    # one to many relationship between Venue and Shows
    shows = db.relationship("Show", backref="venue", lazy=True)

    def __repr__(self):
        return f"<Venue {self.id} {self.name}>"


class Artist(db.Model):
    __tablename__ = "Artist"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    # genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(120))

    # many to many
    genres = db.relationship(
        "Genre", secondary=artist_genre_table, backref=db.backref("artists")
    )

    # one to many
    shows = db.relationship("Show", backref="artist", lazy=True)

    def __repr__(self):
        return f"<Artist {self.id} {self.name}>"


class Show(db.Model):
    __tablename__ = "Show"

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    artist_id = db.Column(db.Integer, db.ForeignKey("Artist.id"), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey("Venue.id"), nullable=False)

    def __repr__(self):
        return f"<Show {self.id} {self.start_time} artist_id={artist_id} venue_id={venue_id}>"