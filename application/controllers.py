from flask import Flask, request,redirect,url_for,flash, session
from flask import render_template
from flask import current_app as app
from application.models import Movie, Cinema, Showtime, Booking, User
from application.database import db
from flask_login import UserMixin, login_user, login_required, logout_user, current_user, LoginManager, login_manager

from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms .widgets import TextArea
from datetime import datetime



# Login configuration
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Create a Form Class
class UserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    # user_username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password_hash = PasswordField("Password",validators=[DataRequired()])
    # password_hash2 = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create a user login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

# Create a booking form
class BookingForm(FlaskForm):
    num_tickets = StringField("Number of Tickets", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create a review form
class ReviewForm(FlaskForm):
    review = TextAreaField("Review", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create a show form
class ShowForm(FlaskForm):
    venue_id = StringField("Venue ID", validators=[DataRequired()])
    movie_id = StringField("Movie ID", validators=[DataRequired()])
    date = StringField("Date", validators=[DataRequired()])
    time = StringField("Time", validators=[DataRequired()])
    ticket_price = StringField("Ticket Price", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create a show edit form
class ShowEditForm(FlaskForm):
    date = StringField("Date", validators=[DataRequired()])
    time = StringField("Time", validators=[DataRequired()])
    ticket_price = StringField("Ticket Price", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create a venue form
class CinemaForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    place = StringField("Place", validators=[DataRequired()])
    capacity = StringField("Capacity", validators=[DataRequired()])
    image_url = StringField("Image URL", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create a CinemaEditForm form
class CinemaEditForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    location = StringField("location", validators=[DataRequired()])
    seating_capacity = StringField("seating_capacity", validators=[DataRequired()])
    # image_url = StringField("Image URL", validators=[DataRequired()])
    # description = TextAreaField("Description", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create a movie form
class MovieForm(FlaskForm):
    name = StringField("Title", validators=[DataRequired()])
    # image_url = StringField("Image URL", validators=[DataRequired()])
    genere = TextAreaField("Genere", validators=[DataRequired()])
    director = StringField("Director", validators=[DataRequired()])
    cast = StringField("Cast", validators=[DataRequired()])
    synopsis = TextAreaField("Synopsis", validators=[DataRequired()])
    duration = StringField("Duration", validators=[DataRequired()])
    release_date = StringField("Release Date", validators=[DataRequired()])
    rating = StringField("Rating", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create a user registration form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


# Create a login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            # Check the Hasssed Password
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("Login Succesfully")
                return redirect(url_for('home'))
            else:
                flash("Wrong Password")
        else:
            flash("User Doesen't Exist")
    return render_template('login.html',form=form)


# Logout

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))





# User Registration 

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = UserForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
        # user.set_password(form.password.data)
        user = User(username=form.username.data, email=form.email.data,password_hash=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)



@app.route("/", methods=["GET", "POST"])
def home():
    movies = Movie.query.all()
    return render_template('home.html', movies=movies)


@app.route('/movies/<int:movie_id>')
def movie_detail(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    showtimes = movie.showtimes
    return render_template('movie_detail.html', movie=movie, showtimes=showtimes)

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    # Check if current user is admin
    if not current_user.is_admin:
        return redirect(url_for('home'))

    show_form = ShowForm()
    cinema_form = CinemaForm()
    movie_form = MovieForm()



    if show_form.validate_on_submit():
        # Retrieve form data
        venue_id = show_form.venue_id.data
        movie_id = show_form.movie_id.data
        date = show_form.date.data
        time = show_form.time.data
        ticket_price = show_form.ticket_price.data  

        # Create a new Showtime object
        show = Showtime(cinema_id=venue_id, movie_id=movie_id, date=date, time=time, ticket_price=ticket_price)

        # Add new show to the database
        db.session.add(show)
        db.session.commit()

        # Flash message to indicate success
        flash('New show added successfully!', 'success')

        # Redirect back to admin page
        return redirect(url_for('admin'))

    if cinema_form.validate_on_submit():
        # Retrieve form data
        name = cinema_form.name.data
        place = cinema_form.place.data
        capacity = cinema_form.capacity.data
        image_url = cinema_form.image_url.data
        description = cinema_form.description.data

        # Create a new Cinema object
        cinema = Cinema(name=name, location=place, seating_capacity=capacity)

        # Add new cinema to the database
        db.session.add(cinema)
        db.session.commit()

        # Flash message to indicate success
        flash('New cinema added successfully!', 'success')

        # Redirect back to admin page
        return redirect(url_for('admin'))
    
    if movie_form.validate_on_submit():
        # Retrieve form data
        name = movie_form.name.data
        # image_url = movie_form.image_url.data
        genere = movie_form.genere.data
        director = movie_form.director.data
        cast = movie_form.cast.data
        synopsis = movie_form.synopsis.data
        duration = movie_form.duration.data
        release_date = movie_form.release_date.data
        rating = movie_form.rating.data

        # Create a new Movie object
        movie = Movie(name=name, genre=genere, director=director, cast=cast, synopsis=synopsis, duration=duration, release_date=release_date, rating=rating)

        # Add new movie to the database
        db.session.add(movie)
        db.session.commit()

        # Flash message to indicate success
        flash('New movie added successfully!', 'success')

        # Redirect back to admin page
        return redirect(url_for('admin'))

    # Get all cinemas from the database
    cinemas = Cinema.query.all()

    # Get all shows from the database
    shows = Showtime.query.all()

    # Get all Movies from the databse
    movies = Movie.query.all()

    return render_template('admin.html', shows=shows, cinemas=cinemas, show_form=show_form, cinema_form=cinema_form, movies=movies, movie_form=movie_form)


@app.route('/admin/delete_movie/<int:id>', methods=['GET','POST'])
@login_required
def delete_movie(id):
    # Check if current user is admin
    if not current_user.is_admin:
        return redirect(url_for('home'))

    # Get movie with the specified ID
    movie = Movie.query.get_or_404(id)

    # Delete movie from database
    db.session.delete(movie)
    db.session.commit()

    # Flash message to indicate success
    flash('Movie deleted successfully!', 'success')

    # Redirect back to admin page
    return redirect(url_for('admin'))


@app.route('/admin/edit_movie/<int:id>', methods=['GET','POST'])
@login_required
def edit_movie(id):     
    # Check if current user is admin
    if not current_user.is_admin:
        return redirect(url_for('home'))

    movie = Movie.query.get_or_404(id)
    movie_form = MovieForm()

    if movie_form.validate_on_submit():
        # Retrieve form data
        name = movie_form.name.data
        # image_url = movie_form.image_url.data
        genere = movie_form.genere.data
        director = movie_form.director.data
        cast = movie_form.cast.data
        synopsis = movie_form.synopsis.data
        duration = movie_form.duration.data
        release_date = movie_form.release_date.data
        rating = movie_form.rating.data

        # Create a new Movie object
        movie = Movie(name=name, genre=genere, director=director, cast=cast, synopsis=synopsis, duration=duration, release_date=release_date, rating=rating)

        # Add new movie to the database
        db.session.add(movie)
        db.session.commit()

        # Flash message to indicate success
        flash('Movie updated successfully!', 'success')

        # Redirect back to admin page
        return redirect(url_for('admin'))

    return render_template('edit_movie.html', movie=movie, movie_form=movie_form)
    



# @app.route('/admin', methods=['GET', 'POST'])
# @login_required
# def admin():
#     # Check if current user is admin
#     if not current_user.is_admin:
#         return redirect(url_for('home'))

#     show_form = ShowForm()
#     # cinema_form = CinemaForm()

#     if show_form.validate_on_submit():
#         # Retrieve form data
#         venue_id = show_form.venue_id.data
#         movie_id = show_form.movie_id.data
#         date = show_form.date.data
#         time = show_form.time.data
#         ticket_price = show_form.ticket_price.data  

#         # Create a new Showtime object
#         show = Showtime(cinema_id=venue_id, movie_id=movie_id, date=date, time=time, ticket_price=ticket_price)

#         # Add new show to the database
#         db.session.add(show)
#         db.session.commit()

#         # Flash message to indicate success
#         flash('New show added successfully!', 'success')

#         # Redirect back to admin page
#         return redirect(url_for('admin'))

#     # if cinema_form.validate_on_submit():
#     #     # Retrieve form data
#     #     name = cinema_form.name.data
#     #     place = cinema_form.place.data
#     #     capacity = cinema_form.capacity.data
#     #     # image_url = cinema_form.image_url.data
#     #     # description = cinema_form.description.data

#     #     # Create a new Cinema object
#     #     cinema = Cinema(name=name, location=place, seating_capacity=capacity)

#     #     # Add new cinema to the database
#     #     db.session.add(cinema)
#     #     db.session.commit()

#         # Flash message to indicate success
#         # flash('New cinema added successfully!', 'success')

#         # Redirect back to admin page
#         # return redirect(url_for('admin'))

#     # Get all cinemas from the database
#     # cinemas = Cinema.query.all()

#     # Get all shows from the database
#     shows = Showtime.query.all()

#     return render_template('admin.html', shows=shows, show_form=show_form)


@app.route('/admin/delete_show/<int:id>', methods=['GET','POST'])
@login_required
def delete_show(id):
    # Check if current user is admin
    if not current_user.is_admin:
        return redirect(url_for('home'))

    # Get show with the specified ID
    show = Showtime.query.get_or_404(id)

    # Delete show from database
    db.session.delete(show)
    db.session.commit()

    # Flash message to indicate success
    flash('Show deleted successfully!', 'success')

    # Redirect back to admin page
    return redirect(url_for('admin'))

@app.route('/admin/edit_show/<int:id>', methods=['GET','POST'])
@login_required
def edit_show(id):
    # Check if current user is admin
    if not current_user.is_admin:
        return redirect(url_for('home'))

    show = Showtime.query.get_or_404(id)
    show_form = ShowEditForm()

    if show_form.validate_on_submit():
        # Retrieve form data
        date = show_form.date.data
        time = show_form.time.data
        ticket_price = show_form.ticket_price.data

        # Update the showtime details
        show.date = date
        show.time = time
        show.ticket_price = ticket_price
        # Commit changes to the database
        db.session.commit()

        # Flash message to indicate success
        flash('Show updated successfully!', 'success')

        # Redirect back to admin page
        return redirect(url_for('admin'))

    return render_template('edit_show.html', show=show, show_form=show_form)

@app.route('/admin/addmovie', methods=['GET', 'POST'])
@login_required
def addmovie():
    # Check if current user is admin
    if not current_user.is_admin:
        return redirect(url_for('home'))

    movie_form = MovieForm()

    if movie_form.validate_on_submit():
        # Retrieve form data
        name = movie_form.name.data
        # image_url = movie_form.image_url.data
        genere = movie_form.genere.data
        director = movie_form.director.data
        cast = movie_form.cast.data
        synopsis = movie_form.synopsis.data
        duration = movie_form.duration.data
        release_date = movie_form.release_date.data
        rating = movie_form.rating.data

        # Create a new Movie object
        movie = Movie(name=name, genre=genere, director=director, cast=cast, synopsis=synopsis, duration=duration, release_date=release_date, rating=rating)

        # Add new movie to the database
        db.session.add(movie)
        db.session.commit()

        # Flash message to indicate success
        flash('New movie added successfully!', 'success')

        # Redirect back to admin page
        return redirect(url_for('admin'))

    return render_template('addmovie.html', movie_form=movie_form)

@app.route('/admin/addcinema', methods=['GET', 'POST'])
@login_required
def addcinema():
    # Check if current user is admin
    if not current_user.is_admin:
        return redirect(url_for('home'))

    cinema_form = CinemaForm()

    if cinema_form.validate_on_submit():
        # Retrieve form data
        name = cinema_form.name.data
        place = cinema_form.place.data
        capacity = cinema_form.capacity.data
        image_url = cinema_form.image_url.data
        description = cinema_form.description.data

        # Create a new Cinema object
        cinema = Cinema(name=name, location=place, seating_capacity=capacity)

        # Add new cinema to the database
        db.session.add(cinema)
        db.session.commit()

        # Flash message to indicate success
        flash('New cinema added successfully!', 'success')

        # Redirect back to admin page
        return redirect(url_for('admin'))

    return render_template('addcinema.html', cinema_form=cinema_form)

@app.route('/admin/edit_cinema/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_cinema(id):
    # Check if current user is admin
    if not current_user.is_admin:
        return redirect(url_for('home'))
    cinemas = Cinema.query.get_or_404(id)
    cinema_form = CinemaEditForm()

    if cinema_form.validate_on_submit():
        # Retrieve form data
        name = cinema_form.name.data
        location = cinema_form.location.data
        capacity = cinema_form.seating_capacity.data


        # Update the cinema details
        cinemas.name = name
        cinemas.location = location
        cinemas.seating_capacity = capacity

        # Commit changes to the database

        db.session.commit()

        # Flash message to indicate success
        flash('Cinema Edited successfully!', 'success')

        # Redirect back to admin page
        return redirect(url_for('admin'))

    return render_template('edit_cinema.html', cinemas=cinemas, cinema_form=cinema_form)

@app.route('/admin/delete_cinema/<int:id>', methods=['GET','POST'])
@login_required
def delete_cinema(id):
    # Check if current user is admin
    if not current_user.is_admin:
        return redirect(url_for('home'))

    # Get cinema with the specified ID
    cinema = Cinema.query.get_or_404(id)

    # Delete cinema from database
    db.session.delete(cinema)
    db.session.commit()

    # Flash message to indicate success
    flash('Cinema deleted successfully!', 'success')

    # Redirect back to admin page
    return redirect(url_for('admin'))


# @app.route('/movies/<int:movie_id>')
# def movie_detail(movie_id):
#     movie = Movie.query.get_or_404(movie_id)
#     showtimes = Showtime.query.filter_by(movie_id=movie_id).all()
#     # for showtime in showtimes:
#     #     showtime.time = datetime.strptime(showtime.time, '%Y-%m-%d %H:%M:%S')
#     return render_template('movie_detail.html', movie=movie, showtimes=showtimes)


# @app.route('/venues')
# def venues():
#     venues = Venue.query.all()
#     return render_template('venues.html', venues=venues)


# @app.route('/shows/<int:show_id>')
# def show_detail(show_id):
#     show = Show.query.get_or_404(show_id)
#     return render_template('show_detail.html', show=show)



# @app.route('/book/<int:show_id>', methods=['GET', 'POST'])
# def book(show_id):
#     show = Show.query.get_or_404(show_id)
#     if request.method == 'POST':
#         num_tickets = int(request.form['num_tickets'])
#         if num_tickets <= 0 or num_tickets > (show.venue.capacity - show.num_booked):
#             flash('Invalid number of tickets.')
#             return redirect(url_for('book', show_id=show.id))
        




# # Route for booking tickets
# @app.route('/book_tickets', methods=['GET', 'POST'])
# def book_tickets():
#     if request.method == 'POST':
#         # Get show and venue ID from form
#         show_id = request.form.get('show_id')
#         venue_id = request.form.get('venue_id')

#         # Query the database for the selected show and venue
#         show = Show.query.get(show_id)
#         venue = Venue.query.get(venue_id)

#         # Get number of tickets to book from form
#         num_tickets = int(request.form.get('num_tickets'))

#         # Check if there are enough seats available
#         if num_tickets > venue.capacity - show.num_booked:
#             return render_template('booking_error.html')

#         # Update the number of booked tickets for the show
#         show.num_booked += num_tickets
#         db.session.commit()

#         # Create a new booking for the user
#         booking = Booking(show_id=show_id, venue_id=venue_id, num_tickets=num_tickets)
#         db.session.add(booking)
#         db.session.commit()

#         return redirect(url_for('booking_confirmation'))

#     # Query the database for all available shows and venues
#     shows = Show.query.all()
#     venues = Venue.query.all()

#     return render_template('book_tickets.html', shows=shows, venues=venues)

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))







# @app.route('/show/new', methods=['GET', 'POST'])
# @login_required
# def new_show():
#     form = ShowForm()
#     form.venue.choices = [(venue.id, venue.name) for venue in Venue.query.order_by('name')]
#     if form.validate_on_submit():
#         show = Show(name=form.name.data, rating=form.rating.data, tags=form.tags.data, 
#                     ticket_price=form.ticket_price.data, venue_id=form.venue.data)
        

#         db.session.add(show)
#         db.session.commit()
#         flash('Your show has been created!')
#         return redirect(url_for('show', show_id=show.id))
#     return render_template('create_show.html', title='New Show', form=form)




# # @app.route('/register', methods=['GET', 'POST'])
# # def register():
# #     if current_user.is_authenticated:
# #         return redirect(url_for('index'))
# #     form = RegistrationForm()
# #     if form.validate_on_submit():
# #         user = User(username=form.username.data, email=form.email.data)
# #         user.set_password(form.password.data)
# #         db.session.add(user)
# #         db.session.commit()
# #         flash('Congratulations, you are now a registered user!')
# #         return redirect(url_for('login'))
# #     return render_template('register.html', title='Register', form=form)

# @app.route('/user/<username>')
# @login_required
# def user(username):
#     user = User.query.filter_by(username=username).first_or_404()
#     return render_template('user.html', user=user)

 
