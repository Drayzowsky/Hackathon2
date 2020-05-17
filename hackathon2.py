from flask import Flask, render_template, request, jsonify, make_response, json
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from pusher import pusher
import simplejson

app = Flask(__name__)
app.config["SECRET_KEY"] = "thisissecretpassword"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:Mamita2019@localhost:5432/hackathon"
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# configure pusher object
pusher = pusher.Pusher(
app_id="1002493",
key="792745e0907fdb507199",
secret="c9c5693de1185d9d3164",
cluster="ap2",
ssl=True)

class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20))
    lastname = db.Column(db.String(20))
    username = db.Column(db.String(20), unique=True)
    adress = db.Column(db.String())
    city = db.Column(db.String())
    country = db.Column(db.String())
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))




class Login(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=100)])


class Signin(FlaskForm):
    firstname = StringField('Firstame', validators=[DataRequired(), Length(min=3, max=20)])
    lastname = StringField('Lastname', validators=[DataRequired(), Length(min=3, max=20)])
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    adress = StringField('Adress', validators=[DataRequired()])
    city= StringField('City', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Length(max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=100)])


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/new/guest', methods=['POST'])
def guestUser():
    data = request.json
    pusher.trigger(u'general-channel', u'new-guest-details', {
        'name' : data['name'],
        'email' : data['email']
        })
    return json.dumps(data)


@app.route("/pusher/auth", methods=['POST'])
def pusher_authentication():
    auth = pusher.authenticate(channel=request.form['channel_name'],socket_id=request.form['socket_id'])
    return json.dumps(auth)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.password == form.password.data:
                return form.username.data
            return "<h1>Enter valid username/password</h1>"

    return render_template("login.html", form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = Signin()
    if form.validate_on_submit():
        new_user = User(firstname=form.firstname.data, lastname=form.lastname.data, username=form.username.data, adress=form.adress.data, city=form.city.data, country=form.country.data,
                        email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return "<h1>New user has been created!</h1>"

    return render_template("signup.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
