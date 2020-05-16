from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config["SECRET_KEY"] = "thisissecretpassword"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:Mamita2019@localhost:5432/hackathon"
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20))
    lastname = db.Column(db.String(20))
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))



class Login(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=100)])


class Signin(FlaskForm):
    firstname = StringField('Firstame', validators=[DataRequired(), Length(min=3, max=20)])
    lastname = StringField('Lastname', validators=[DataRequired(), Length(min=3, max=20)])
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Length(max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=100)])


@app.route("/")
def index():
    return render_template("index.html")


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
        new_user = User(firstname=form.firstname.data, lastname=form.lastname.data, username=form.username.data,
                        email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return "<h1>New user has been created!</h1>"

    return render_template("signup.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
