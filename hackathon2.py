from flask import Flask, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config["SECRET_KEY"] = "thisissecretpassword"
bootstrap = Bootstrap(app)


class Login(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=8, max=100)])


class Signin(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Length(max=50)])
    username = StringField('username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=8, max=100)])


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = Login()
    return render_template("login.html", form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = Signin()
    return render_template("signup.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)