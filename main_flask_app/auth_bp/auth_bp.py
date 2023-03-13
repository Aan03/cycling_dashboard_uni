from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from flask_login import UserMixin, login_required, current_user, login_user, LoginManager, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
import wtforms

from main_flask_app.dash_app_cycling import *
from main_flask_app import db
from main_flask_app.models import user


auth_bp = Blueprint('auth_bp', __name__, template_folder = "templates")

class LoginForm(FlaskForm):
    username = StringField("Username")#, validators=[DataRequired()])
    password = PasswordField("Password")#, validators=[DataRequired()])
    submit = SubmitField("Submit")

@auth_bp.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    return render_template('profile.html')#name=current_user.name)

@auth_bp.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if request.method == "GET":
        return render_template('login.html', form = form)

    elif request.method == "POST":
        usernamee = request.form['username']
        passwordd = request.form['password']
        user_check = user.query.filter_by(username=usernamee).first()
        if not user_check or passwordd != user_check.password:
            flash('Please check your login details and try again.')
            return redirect(url_for('auth_bp.login')) 

        if user_check:
            if (passwordd == user_check.password):
                login_user(user_check, remember="remember")
                return redirect(url_for('auth_bp.profile'))
            else:
                flash("Try password again")

@auth_bp.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main_bp.index'))

@auth_bp.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    # code to validate and add user to database goes here
    if request.method == "GET":
        return render_template('sign_up.html')
    elif request.method == "POST":
        usernamee = request.form['username']
        passwordd = request.form['password']

        user_check = user.query.filter_by(username=usernamee).first()
        if user_check:
            flash("Username taken...")
            return redirect(url_for('auth_bp.sign_up'))

#
    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = user(username=usernamee, password=passwordd)#generate_password_hash(password, method='sha256'))

    # add the new user to the database
        try:
            db.session.add(new_user)
            db.session.commit()
            #print(db.Query("username"))
            return redirect(url_for('auth_bp.login'))
           # return db.Query("username")
        except:
            return "error adding"