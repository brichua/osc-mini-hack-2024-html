from flask import Flask, render_template, url_for, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField 
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'
db = SQLAlchemy(app)
app.app_context().push()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#Make Table
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    clubs = db.relationship('Club', backref='user')
    

class Club(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cName = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#Register Form
class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            flash("That username already exists. Please choose a different one.")
            raise ValidationError(
                'That username already exists. Please choose a different one.')

#Login Form
class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')

    

#Club Form
class ClubForm(FlaskForm):
    cName = StringField(validators=[
                           InputRequired(), Length(min=2, max=120)], render_kw={"placeholder": "Club Name"})
    submit = SubmitField('Add')    


        

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                session["user"] = user.username
                session["id"] = user.id
                login_user(user)
                return redirect(url_for('home'))  
            flash("Incorrect password. Try again!")
        else:
            flash("Username does not exist")
    return render_template('login.html', form = form)

@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    form = ClubForm()
    if form.validate_on_submit():
        club = Club.query.filter_by(cName = form.cName.data, user_id = current_user.id).first()
        if club:
            flash('Club already added')
        else:    
            new_club = Club(cName = form.cName.data, user_id = session["id"])
            db.session.add(new_club)
            db.session.commit()
            return redirect(url_for('home'))
    aClub = Club.query.filter_by(user_id = current_user.id).all()
    clubs = [] 
    for x in range(len(aClub)):
        clubs.append(aClub[x].cName)
    
    return render_template('home.html', name = current_user.username, form = form, clubs = clubs)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    
    return render_template('signup.html', form = form)

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    session.pop("user" , None)
    session.pop("id", None)
    logout_user()
    return redirect(url_for('login'))

@app.route('/profile', methods = ['GET', 'POST'])
def profile():
    aClub = Club.query.filter_by(user_id = current_user.id).all()
    clubs = [] 
    for x in range(len(aClub)):
        clubs.append(aClub[x].cName)
    return render_template('profile.html', name = current_user.username, clubs=clubs)

@app.route('/search', methods = ['GET', 'POST'])
def search():
    return render_template('search.html')

@app.route('/calendar', methods = ['GET', 'POST'])
def calendar():
    return render_template('calendar.html')

@app.route('/following', methods = ['GET', 'POST'])
def following():
    return render_template('following.html')

if __name__ == '__main__':
    app.run(debug=True)