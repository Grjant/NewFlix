from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData
import os
app = Flask(__name__)
# move to env file later
USER = "newflixdb"
PASSWORD = "Password123"
PUBLIC_IP_ADDRESS = "35.238.32.41"
DBNAME = "newflixdb"

# configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{USER}:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}'
# to suppress a warning message
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

link = db.Table('link',
                db.Column('streamingservice_id', db.Integer,
                          db.ForeignKey('streamingservice.id')),
                db.Column('movie_id', db.String(100),
                          db.ForeignKey('movie.id'))
                )


class Theater(db.Model):
    # Theater model describes a theater.
    __tablename__ = 'theater'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    google_maps = db.Column(db.String(5000), nullable=False)
    img = db.Column(db.String(200), nullable=False)

    showings = db.relationship('Showings', backref='theater')


class Showings(db.Model):
    # Showings model describes a showing, which is an instance of a movie shown at a theater.
    __tablename__ = 'showings'
    id = db.Column(db.Integer, primary_key=True)
    theater_id = db.Column(db.Integer, db.ForeignKey(
        'theater.id'))
    movie_id = db.Column(db.String(100), db.ForeignKey(
        'movie.id'))
    day = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(200))
    times = db.relationship('Time', backref='showing')


class Time(db.Model): 
    # Time model describes the times that showings happen. 
    __tablename__ = 'time'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(200))
    showings_id = db.Column(db.Integer, db.ForeignKey(
        'showings.id'))


class Movie(db.Model):
    # Movie model describes a movie. 
    __tablename__ = 'movie'

    title = db.Column(db.String(80), nullable=False)
    id = db.Column(db.String(100), primary_key=True)
    poster = db.Column(db.String(200), nullable=False)
    duration = db.Column(db.String(80), nullable=False)
    genre = db.Column(db.String(80), nullable=False)
    rotten_tomatoes_rating = db.Column(db.String(80), nullable=False)
    imdb_rating = db.Column(db.String(80), nullable=False)
    director = db.Column(db.String(80), nullable=False)
    plot = db.Column(db.String(500), nullable=False)
    showings = db.relationship('Showings', backref='movie')


class StreamingService(db.Model):
    # StreamingService model describes a streaming service. 
    __tablename__ = 'streamingservice'

    name = db.Column(db.String(80), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    logo = db.Column(db.String(200), nullable=False)
    website = db.Column(db.String(250))
    country_origin = db.Column(db.String(40))
    base_price = db.Column(db.Float)
    ad_free_available = db.Column(db.String(3))
    revenue2022 = db.Column(db.Float)
    user_base = db.Column(db.Float)
    movies = db.relationship('Movie', secondary='link', backref='streams')
