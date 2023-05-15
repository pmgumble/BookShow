
from flask_restful import Resource, Api
from flask_restful import fields, marshal_with
from flask_restful import reqparse, request
from application.models import User, Movie, Cinema, Booking, Comment, Like, Showtime
from application.database import db
from flask import current_app as app, jsonify, g, url_for, request, make_response
import werkzeug
from flask import abort
from werkzeug.security import generate_password_hash, check_password_hash
from application.validation import NotFoundError, BusinessValidationError


from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()



# API for creating a new cinema object
class CinemaAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, required=True, help='No cinema name provided', location='json')
        self.reqparse.add_argument('location', type=str, required=True, help='No cinema location provided', location='json')
        self.reqparse.add_argument('seating_capacity', type=int, required=True, help='No cinema seating capacity provided', location='json')
        super(CinemaAPI, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        cinema = Cinema(name=args['name'], location=args['location'],seating_capacity=args['seating_capacity'])
        db.session.add(cinema)
        db.session.commit()
        return {'status': 'success', 'data': cinema.serialize()}, 201
    
    def get(self):
        cinemas = Cinema.query.all()
        return {'status': 'success', 'data': [cinema.serialize() for cinema in cinemas]}, 200
    def delete(self):
        cinemas = Cinema.query.all()
        for cinema in cinemas:
            db.session.delete(cinema)
        db.session.commit()
        return {'status': 'success', 'data': 'All cinemas deleted'}, 200
    def put(self):
        args = self.reqparse.parse_args()
        cinema = Cinema.query.filter_by(name=args['name']).first()
        cinema.location = args['location']
        cinema.seating_capacity = args['seating_capacity']
        db.session.commit()
        return {'status': 'success', 'data': cinema.serialize()}, 200

# API for creating a new movie object
class MovieAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, required=True, help='No movie name provided', location='json')
        self.reqparse.add_argument('genre', type=str, required=True, help='No movie genre provided', location='json')
        self.reqparse.add_argument('director', type=str, required=True, help='No movie director provided', location='json')
        self.reqparse.add_argument('cast', type=str, required=True, help='No movie cast provided', location='json')
        self.reqparse.add_argument('synopsis', type=str, required=True, help='No movie synopsis provided', location='json')
        self.reqparse.add_argument('duration', type=int, required=True, help='No movie duration provided', location='json')
        self.reqparse.add_argument('release_date', type=str, required=True, help='No movie release date provided', location='json')
        self.reqparse.add_argument('rating', type=float, required=True, help='No movie rating provided', location='json')
        # self.reqparse.add_argument('poster', type=str, required=True, help='No movie poster provided', location='json')
        super(MovieAPI, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        movie = Movie(name=args['name'], genre=args['genre'], director=args['director'], cast=args['cast'], synopsis=args['synopsis'], duration=args['duration'], release_date=args['release_date'], rating=args['rating'])
        db.session.add(movie)
        db.session.commit()
        return {'status': 'success', 'data': movie.serialize()}, 201
    
    def get(self):
        movies = Movie.query.all()
        return {'status': 'success', 'data': [movie.serialize() for movie in movies]}, 200
    def delete(self):
        movies = Movie.query.all()
        for movie in movies:
            db.session.delete(movie)
        db.session.commit()
        return {'status': 'success', 'data': 'All movies deleted'}, 200
    def put(self):
        args = self.reqparse.parse_args()
        movie = Movie.query.filter_by(name=args['name']).first()
        movie.genre = args['genre']
        movie.director = args['director']
        movie.cast = args['cast']
        movie.synopsis = args['synopsis ']
        movie.duration = args['duration']
        movie.release_date = args['release_date']
        movie.rating = args['rating']
        db.session.commit()
        return {'status': 'success', 'data': movie.serialize()}, 200
    
# API for creating a new showtime object
class ShowtimeAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('movie_id', type=int, required=True, help='No movie id provided', location='json')
        self.reqparse.add_argument('cinema_id', type=int, required=True, help='No cinema id provided', location='json')
        self.reqparse.add_argument('date', type=str, required=True, help='No date provided', location='json')
        self.reqparse.add_argument('time', type=str, required=True, help='No time provided', location='json')
        self.reqparse.add_argument('ticket_price', type=float, required=True, help='No ticket price provided', location='json')

        super(ShowtimeAPI, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        showtime = Showtime(movie_id=args['movie_id'], cinema_id=args['cinema_id'], date=args['date'], time=args['time'], ticket_price=args['ticket_price'])
        db.session.add(showtime)
        db.session.commit()
        return {'status': 'success', 'data': showtime.serialize()}, 201
    
    def get(self):
        showtimes = Showtime.query.all()
        return {'status': 'success', 'data': [showtime.serialize() for showtime in showtimes]}, 200
    def delete(self):
        showtimes = Showtime.query.all()
        for showtime in showtimes:
            db.session.delete(showtime)
        db.session.commit()
        return {'status': 'success', 'data': 'All showtimes deleted'}, 200
    def put(self):
        args = self.reqparse.parse_args()
        showtime = Showtime.query.filter_by(movie_id=args['movie_id'], cinema_id=args['cinema_id']).first()
        showtime.showtime = args['showtime']
        db.session.commit()
        return {'status': 'success', 'data': showtime.serialize()}, 200
    
# API for creating a new user object
class UserAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, required=True, help='No username provided', location='json')
        self.reqparse.add_argument('email', type=str, required=True, help='No email provided', location='json')
        self.reqparse.add_argument('password', type=str, required=True, help='No password provided', location='json')
        super(UserAPI, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        user = User(username=args['username'], email=args['email'])
        user.password = args['password']
        db.session.add(user)
        db.session.commit()
        return {'status': 'success', 'data': user.serialize()}, 201
    
    def get(self):
        users = User.query.all()
        return {'status': 'success', 'data': [user.serialize() for user in users]}, 200
    def delete(self):
        users = User.query.all()
        for user in users:
            db.session.delete(user)
        db.session.commit()
        return {'status': 'success', 'data': 'All users deleted'}, 200
    def put(self):
        args = self.reqparse.parse_args()
        user = User.query.filter_by(username=args['username']).first()
        user.email = args['email']
        user.password = args['password']
        db.session.commit()
        return {'status': 'success', 'data': user.serialize()}, 200

# API for creating a new booking object
class BookingAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('user_id', type=int, required=True, help='No user id provided', location='json')
        self.reqparse.add_argument('movie_id', type=int, required=True, help='No movie id provided', location='json')
        self.reqparse.add_argument('showtime_id', type=int, required=True, help='No showtime id provided', location='json')
        self.reqparse.add_argument('seats', type=int, required=True, help='No seats provided', location='json')
        super(BookingAPI, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        booking = Booking(user_id=args['user_id'], movie_id=args['movie_id'], showtime_id=args['showtime_id'], seats=args['seats'])
        db.session.add(booking)
        db.session.commit()
        return {'status': 'success', 'data': booking.serialize()}, 201
    
    def get(self):
        bookings = Booking.query.all()
        return {'status': 'success', 'data': [booking.serialize() for booking in bookings]}, 200
    def delete(self):
        bookings = Booking.query.all()
        for booking in bookings:
            db.session.delete(booking)
        db.session.commit()
        return {'status': 'success', 'data': 'All bookings deleted'}, 200
    def put(self):
        args = self.reqparse.parse_args()
        booking = Booking.query.filter_by(user_id=args['user_id'], movie_id=args['movie_id'], showtime_id=args['showtime_id']).first()
        booking.seats = args['seats']
        db.session.commit()
        return {'status': 'success', 'data': booking.serialize()}, 200


# API for getting all the movies
class MoviesAPI(Resource):
    def get(self):
        movies = Movie.query.all()
        return {'status': 'success', 'data': [movie.serialize() for movie in movies]}, 200
    

# API for getting all the cinemas
class CinemasAPI(Resource): 
    def get(self):
        cinemas = Cinema.query.all()
        return {'status': 'success', 'data': [cinema.serialize() for cinema in cinemas]}, 200
    
# API for getting all the showtimes
class ShowtimesAPI(Resource):
    def get(self):
        showtimes = Showtime.query.all()
        return {'status': 'success', 'data': [showtime.serialize() for showtime in showtimes]}, 200

# API for getting all the users
class UsersAPI(Resource):
    def get(self):
        users = User.query.all()
        return {'status': 'success', 'data': [user.serialize() for user in users]}, 200

# API for getting all the bookings
class BookingsAPI(Resource):
    def get(self):
        bookings = Booking.query.all()
        return {'status': 'success', 'data': [booking.serialize() for booking in bookings]}, 200

# API for getting all the comments

class CommentsAPI(Resource):
    def get(self):
        comments = Comment.query.all()
        return {'status': 'success', 'data': [comment.serialize() for comment in comments]}, 200

# API for getting all the likes
class LikesAPI(Resource):
    def get(self):
        likes = Like.query.all()
        return {'status': 'success', 'data': [like.serialize() for like in likes]}, 200

# API for getting a specific movie
class MovieAPI(Resource):
    def get(self, movie_id):
        movie = Movie.query.filter_by(id=movie_id).first()
        if movie is None:
            raise NotFoundError(404)
        return {'status': 'success', 'data': movie.serialize()}, 200

# API for getting a specific cinema
class CinemaAPI(Resource):
    def get(self, cinema_id):
        cinema = Cinema.query.filter_by(id=cinema_id).first()
        if cinema is None:
            raise NotFoundError(404)
        return {'status': 'success', 'data': cinema.serialize()}, 200

# # API for getting a specific showtime
# class ShowtimeAPI(Resource):
#     def get(self, showtime_id):
#         showtime = Showtime.query.filter_by(id=showtime_id).first()
#         if showtime is None:
#             raise NotFoundError(404)
#         return {'status': 'success', 'data': showtime.serialize()}, 200

# # API for getting a specific user
# class UserAPI(Resource):
#     def get(self, user_id):
#         user = User.query.filter_by(id=user_id).first()
#         if user is None:
#             raise NotFoundError(404)
#         return {'status': 'success', 'data': user.serialize()}, 200

# # API for getting a specific booking
# class BookingAPI(Resource):
#     def get(self, booking_id):
#         booking = Booking.query.filter_by(id=booking_id).first()
#         if booking is None:
#             raise NotFoundError(404)
#         return {'status': 'success', 'data': booking.serialize()}, 200

# # API for getting a specific comment
# class CommentAPI(Resource):
#     def get(self, comment_id):
#         comment = Comment.query.filter_by(id=comment_id).first()
#         if comment is None:
#             raise NotFoundError(404)
#         return {'status': 'success', 'data': comment.serialize()}, 200

# # API for getting a specific like
# class LikeAPI(Resource):
#     def get(self, like_id):
#         like = Like.query.filter_by(id=like_id).first()
#         if like is None:
#             raise NotFoundError(404)
#         return {'status': 'success', 'data': like.serialize()}, 200

# # API for getting all the movies of a specific genre
# class GenreAPI(Resource):
#     def get(self, genre):
#         movies = Movie.query.filter_by(genre=genre).all()
#         if movies is None:
#             raise NotFoundError(404)
#         return {'status': 'success', 'data': [movie.serialize() for movie in movies]}, 200
    
# # API for getting all the movies of a specific director
# class DirectorAPI(Resource):
#     def get(self, director):
#         movies = Movie.query.filter_by(director=director).all()
#         if movies is None:
#             raise NotFoundError(404)
#         return {'status': 'success', 'data': [movie.serialize() for movie in movies]}, 200

# # API for getting all the movies of a specific cast
# class CastAPI(Resource):
#     def get(self, cast):
#         movies = Movie.query.filter_by(cast=cast).all()
#         if movies is None:
#             raise NotFoundError(404)
#         return {'status': 'success', 'data': [movie.serialize() for movie in movies]}, 200

# # API for getting all the movies of a specific rating
# class RatingAPI(Resource):
#     def get(self, rating):
#         movies = Movie.query.filter_by(rating=rating).all()
#         if movies is None:
#             raise NotFoundError(404)
#         return {'status': 'success', 'data': [movie.serialize() for movie in movies]}, 200

# # API for getting all the movies of a specific release date
# class ReleaseDateAPI(Resource):
#     def get(self, release_date):
#         movies = Movie.query.filter_by(release_date=release_date).all()
#         if movies is None:
#             raise NotFoundError(404)
#         return {'status': 'success', 'data': [movie.serialize() for movie in movies]}, 200

# # API for getting all the movies of a specific duration
# class DurationAPI(Resource):
#     def get(self, duration):
#         movies = Movie.query.filter_by(duration=duration).all()
#         if movies is None:
#             raise NotFoundError(404)
#         return {'status': 'success', 'data': [movie.serialize() for movie in movies]}, 200

# # API for getting all the movies of a specific showtime
# class ShowtimeAPI(Resource):
#     def get(self, showtime):
#         showtimes = Showtime.query.filter_by(showtime=showtime).all()
#         if showtimes is None:
#             raise NotFoundError(404)
#         return {'status': 'success', 'data': [showtime.serialize() for showtime in showtimes]}, 200

# # API for getting all the movies of a specific location
# class LocationAPI(Resource):
#     def get(self, location):
#         cinemas = Cinema.query.filter_by(location=location).all()
#         if cinemas is None:
#             raise NotFoundError(404)
#         return {'status': 'success', 'data': [cinema.serialize() for cinema in cinemas]}, 200



@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})

@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    print(user)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        print(user)
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


