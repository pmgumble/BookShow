from .database import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    # password = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(128),nullable=True)
    bookings = db.relationship('Booking', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)
    likes = db.relationship('Like', backref='user', lazy=True)

    @property
    def password(self):
        raise AttributeError('Password is not a redable Attribute! ')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    


    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

        # create a string 
    def __repr__(self):
        return '<Name %r>' %self.name


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    director = db.Column(db.String(100), nullable=False)
    cast = db.Column(db.String(1000), nullable=False)
    synopsis = db.Column(db.Text, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    release_date = db.Column(db.Text)
    rating = db.Column(db.Float, nullable=False)
    # poster = db.Column(db.String(100), nullable=False)
    bookings = db.relationship('Booking', backref='movie', lazy=True)
    comments = db.relationship('Comment', backref='movie', lazy=True)
    likes = db.relationship('Like', backref='movie', lazy=True)
    showtimes = db.relationship('Showtime', backref='movie', lazy=True)



class Cinema(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    seating_capacity = db.Column(db.Integer, nullable=False)
    showtimes = db.relationship('Showtime', backref='cinema', lazy=True)




class Showtime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    cinema_id = db.Column(db.Integer, db.ForeignKey('cinema.id'), nullable=False)
    date = db.Column(db.String)
    time = db.Column(db.String, nullable=False)
    ticket_price = db.Column(db.Float, nullable=False)
    bookings = db.relationship('Booking', backref='showtime', lazy=True)




class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    showtime_id = db.Column(db.Integer, db.ForeignKey('showtime.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    cinema_id = db.Column(db.Integer, db.ForeignKey('cinema.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    num_tickets = db.Column(db.Integer, nullable=False)
    # show_id = db.Column(db.Integer, db.ForeignKey('show.id'), nullable=False)
    # # show = db.relationship('Show', backref=db.backref('bookings', lazy=True))

# class Venue(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     place = db.Column(db.String(100), nullable=False)
#     capacity = db.Column(db.Integer, nullable=False)
#     shows = db.relationship('Show', backref='venue', lazy=True)

# class Show(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     rating = db.Column(db.Float, nullable=False)
#     tags = db.Column(db.String(1000), nullable=False)
#     ticket_price = db.Column(db.Float, nullable=False)
#     venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
#     bookings = db.relationship('Booking', backref='show', lazy=True)
#     comments = db.relationship('Comment', backref='show', lazy=True)
#     likes = db.relationship('Like', backref='show', lazy=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    text = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


# Like model
class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)