from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from flask_login import UserMixin, login_required, current_user, login_user, LoginManager, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from main_flask_app.dash_app_cycling import *
from main_flask_app import db
from main_flask_app.models import Users
from passlib.hash import sha256_crypt

auth_bp = Blueprint('auth_bp', __name__, template_folder = "templates")

class LoginForm(FlaskForm):
    username = StringField("Username")#, validators=[DataRequired()])
    password = PasswordField("Password")#, validators=[DataRequired()])
    submit = SubmitField("Submit")

@auth_bp.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    return render_template('profile.html')

@auth_bp.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if request.method == "GET":
        return render_template('login.html', form = form)

    elif request.method == "POST":
        username_flask = request.form['username']
        password_flask = request.form['password']
        user_check = Users.query.filter_by(username=username_flask).first()
        if not user_check or sha256_crypt.verify(password_flask, user_check.password) == False:
            flash('Please check your login details and try again.')
            return redirect(url_for('auth_bp.login')) 

        if user_check:
            if sha256_crypt.verify(password_flask, user_check.password):
                login_user(user_check)
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
    if request.method == "GET":
        return render_template('sign_up.html')
    elif request.method == "POST":
        username_flask = request.form['username']
        
        password_flask = request.form['password']
        encrypted_password = sha256_crypt.encrypt(password_flask)

        user_check = Users.query.filter_by(username=username_flask).first()
        if user_check:
            flash("Username taken...")
            return redirect(url_for('auth_bp.sign_up'))

        new_user = Users(username=username_flask, password=encrypted_password)

    # add the new user to the database
        try:
            db.session.add(new_user)
            db.session.commit()
            #print(db.Query("username"))
            return redirect(url_for('auth_bp.login'))
           # return db.Query("username")
        except:
            return "error adding"