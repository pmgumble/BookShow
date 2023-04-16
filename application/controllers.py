from flask import Flask, request,redirect,url_for,flash, session
from flask import render_template
from flask import current_app as app
from application.models import Movie, Cinema, Showtime, Booking, Venue, Show, User
from application.database import db
from flask_login import UserMixin, login_user, login_required, logout_user, current_user, LoginManager, login_manager

from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms .widgets import TextArea



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
    submit = SubmitField("Submit")

# Create a venue form
class VenueForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    place = StringField("Place", validators=[DataRequired()])
    capacity = StringField("Capacity", validators=[DataRequired()])
    image_url = StringField("Image URL", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create a movie form
class MovieForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    image_url = StringField("Image URL", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
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
    showtimes = Showtime.query.filter_by(movie_id=movie_id).all()
    return render_template('movie_detail.html', movie=movie, showtimes=showtimes)


@app.route('/venues')
def venues():
    venues = Venue.query.all()
    return render_template('venues.html', venues=venues)


@app.route('/shows/<int:show_id>')
def show_detail(show_id):
    show = Show.query.get_or_404(show_id)
    return render_template('show_detail.html', show=show)



@app.route('/book/<int:show_id>', methods=['GET', 'POST'])
def book(show_id):
    show = Show.query.get_or_404(show_id)
    if request.method == 'POST':
        num_tickets = int(request.form['num_tickets'])
        if num_tickets <= 0 or num_tickets > (show.venue.capacity - show.num_booked):
            flash('Invalid number of tickets.')
            return redirect(url_for('book', show_id=show.id))
        

@app.route('/admin')
def admin():
    if 'user_id' not in session or not User.query.get(session['user_id']).is_admin:
        return redirect(url_for('home'))
    shows = Show.query.all()
    venues = Venue.query.all()
    return render_template('admin.html', shows=shows, venues=venues)


@app.route('/admin/create_venue', methods=['GET', 'POST'])
def create_venue():
    if 'user_id' not in session or not User.query.get(session['user_id']).is_admin:
        return redirect(url_for('home'))
    if request.method == 'POST':
        name = request.form['name']
        place = request.form['place']
        capacity = int(request.form['capacity'])
        image_url = request.form['image_url']
        description = request.form['description']
        venue = Venue(name=name, place=place, capacity=capacity, image_url=image_url, description=description)
        db.session.add(venue)
        db.session.commit()
        flash('Venue created successfully!')
        return redirect(url_for('admin'))
    return render_template('create_venue.html')


@app.route('/admin/edit_venue/<int:venue_id>', methods=['GET', 'POST'])
def edit_venue(venue_id):
    if 'user_id' not in session or not User.query.get(session['user_id']).is_admin:
        return redirect(url_for('home'))
    venue = Venue.query.get_or_404(venue_id)
    if request.method == 'POST':
        venue.name = request.form['name']
        venue.place = request.form['place']
        venue.capacity = int(request.form['capacity'])
        venue.image_url = request.form['image_url']
        venue.description = request.form['description']
        db.session.commit()
        flash('Venue updated successfully!')
        return redirect(url_for('admin'))
    return render_template('edit_venue.html', venue=venue)

@app.route('/admin/delete_venue/<int:venue_id>', methods=['GET', 'POST'])
def delete_venue(venue_id):
    if 'user_id' not in session or not User.query.get(session['user_id']).is_admin:
        return redirect(url_for('home'))
    venue = Venue.query.get_or_404(venue_id)
    if request.method == 'POST':
        db.session.delete(venue)
        db.session.commit()
        flash('Venue deleted successfully!')
        return redirect(url_for('admin'))
    return render_template('delete_venue.html', venue=venue)

@app.route('/admin/create_show', methods=['GET', 'POST'])
def create_show():
    if 'user_id' not in session or not User.query.get(session['user_id']).is_admin:
        return redirect(url_for('home'))
    venues = Venue.query.all()
    if request.method == 'POST':
        name = request.form['name']
        rating = float(request.form['rating'])
        tags = request.form['tags']
        ticket_price = float(request.form['ticket_price'])
        venue_id = int(request.form['venue'])
        venue = Venue.query.get_or_404(venue_id)
        show = Show(name=name, rating=rating, tags=tags, ticket_price=ticket_price, venue=venue)
        db.session.add(show)
        db.session.commit()
        flash('Show created successfully!')
        return redirect(url_for('admin'))
    return render_template('create_show.html', venues=venues)

@app.route('/admin/edit_show/<int:show_id>', methods=['GET', 'POST'])
def edit_show(show_id):
    if 'user_id' not in session or not User.query.get(session['user_id']).is_admin:
        return redirect(url_for('home'))
    


# Route for booking tickets
@app.route('/book_tickets', methods=['GET', 'POST'])
def book_tickets():
    if request.method == 'POST':
        # Get show and venue ID from form
        show_id = request.form.get('show_id')
        venue_id = request.form.get('venue_id')

        # Query the database for the selected show and venue
        show = Show.query.get(show_id)
        venue = Venue.query.get(venue_id)

        # Get number of tickets to book from form
        num_tickets = int(request.form.get('num_tickets'))

        # Check if there are enough seats available
        if num_tickets > venue.capacity - show.num_booked:
            return render_template('booking_error.html')

        # Update the number of booked tickets for the show
        show.num_booked += num_tickets
        db.session.commit()

        # Create a new booking for the user
        booking = Booking(show_id=show_id, venue_id=venue_id, num_tickets=num_tickets)
        db.session.add(booking)
        db.session.commit()

        return redirect(url_for('booking_confirmation'))

    # Query the database for all available shows and venues
    shows = Show.query.all()
    venues = Venue.query.all()

    return render_template('book_tickets.html', shows=shows, venues=venues)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




@app.route('/venue/new', methods=['GET', 'POST'])
@login_required
def new_venue():
    form = VenueForm()
    if form.validate_on_submit():
        venue = Venue(name=form.name.data, location=form.location.data, capacity=form.capacity.data)
        db.session.add(venue)
        db.session.commit()
        flash('Your venue has been created!')
        return redirect(url_for('venue', venue_id=venue.id))
    return render_template('create_venue.html', title='New Venue', form=form)


@app.route('/show/new', methods=['GET', 'POST'])
@login_required
def new_show():
    form = ShowForm()
    form.venue.choices = [(venue.id, venue.name) for venue in Venue.query.order_by('name')]
    if form.validate_on_submit():
        show = Show(name=form.name.data, rating=form.rating.data, tags=form.tags.data, 
                    ticket_price=form.ticket_price.data, venue_id=form.venue.data)
        

        db.session.add(show)
        db.session.commit()
        flash('Your show has been created!')
        return redirect(url_for('show', show_id=show.id))
    return render_template('create_show.html', title='New Show', form=form)

# @app.route('/venue/<int:venue_id>/edit', methods=['GET', 'POST'])
# @login_required
# def edit_venue(venue_id):
#     venue = Venue.query.get_or_404(venue_id)
#     form = VenueForm()
#     if form.validate_on_submit():
#         venue.name = form.name.data
#         venue.location = form.location.data
#         venue.capacity = form.capacity.data
#         db.session.commit()
#         flash('Your venue has been updated!')
#         return redirect(url_for('venue', venue_id=venue.id))
#     elif request.method == 'GET':
#         form.name.data = venue.name
#         form.location.data = venue.location
#         form.capacity.data = venue.capacity
#     return render_template('edit_venue.html', title='Edit Venue', form=form)



# @app.route('/show/<int:show_id>/edit', methods=['GET', 'POST'])
# @login_required
# def edit_show(show_id):
#     show = Show.query.get_or_404(show_id)
#     form = ShowForm()
#     form.venue.choices = [(venue.id, venue.name) for venue in Venue.query.order_by('name')]
#     if form.validate_on_submit():
#         show.name = form.name.data
#         show.rating = form.rating.data
#         show.tags = form.tags.data
#         show.ticket_price = form.ticket_price.data
#         show.venue_id = form.venue.data
#         db.session.commit()
#         flash('Your show has been updated!')
#         return redirect(url_for('show', show_id=show.id))
#     elif request.method == 'GET':
#         form.name.data = show.name
#         form.rating.data = show.rating
#         form.tags.data = show.tags
#         form.ticket_price.data = show.ticket_price
#         form.venue.data = show.venue_id
#     return render_template('edit_show.html', title='Edit Show', form=form)

# @app.route('/venue/<int:venue_id>/delete', methods=['POST'])
# @login_required
# def delete_venue(venue_id):
#     venue = Venue.query.get_or_404(venue_id)
#     db.session.delete(venue)
#     db.session.commit()
#     flash('Your venue has been deleted!')
#     return redirect(url_for('index'))

@app.route('/show/<int:show_id>/delete', methods=['POST'])
@login_required
def delete_show(show_id):
    show = Show.query.get_or_404(show_id)
    db.session.delete(show)
    db.session.commit()
    flash('Your show has been deleted!')
    return redirect(url_for('index'))

# @app.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('index'))



# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         user = User(username=form.username.data, email=form.email.data)
#         user.set_password(form.password.data)
#         db.session.add(user)
#         db.session.commit()
#         flash('Congratulations, you are now a registered user!')
#         return redirect(url_for('login'))
#     return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

 
