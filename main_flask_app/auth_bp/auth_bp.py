from flask import Blueprint, render_template, redirect, url_for
from flask import request, flash, current_app
from flask_login import login_required, current_user, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from main_flask_app.dash_app_cycling import *
from main_flask_app import db
from main_flask_app.models import Users
from passlib.hash import sha256_crypt

auth_bp = Blueprint('auth_bp', __name__,
                    template_folder="templates")


# Classes for forms
class LoginForm(FlaskForm):
    username = StringField("Username:", validators=[
        validators.DataRequired()])
    password = PasswordField("Password:", validators=[
        validators.DataRequired()])
    submit = SubmitField("Login")


class SignUpForm(FlaskForm):
    username = StringField("Username:", validators=[
        validators.DataRequired()])
    password = PasswordField("Password:", validators=[
        validators.DataRequired()])
    submit = SubmitField("Sign Up")


class ChangePassword(FlaskForm):
    password_current = PasswordField("Enter your current password:",
                                     validators=[validators.DataRequired()])
    password_new = PasswordField("Enter your new password:",
                                 validators=[validators.DataRequired()])
    submit = SubmitField("Change Password")


# Login users
@auth_bp.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    if request.method == "GET":
        return render_template('login.html', login_form=login_form)

    elif request.method == "POST":
        username_flask = (request.form['username']).lower()
        password_flask = request.form['password']
        user_check = Users.query.filter_by(username=username_flask).first()
  
        if not user_check or sha256_crypt.verify(password_flask,
                                                 user_check.password) == False:
            flash('Please check your login details and try again.')
            return redirect(url_for('auth_bp.login'))

        if user_check:
            if sha256_crypt.verify(password_flask, user_check.password):
                login_user(user_check)
                return redirect(url_for('main_bp.my_reports'))
            else:
                flash("Incorrect password. Try again.")


# Allow users to change their passwords
@auth_bp.route('/account', methods=['POST', 'GET'])
@login_required
def user_account():
    update_password_form = ChangePassword()
    if request.method == "GET":
        return render_template('account.html',
                               update_password_form=update_password_form)

    elif request.method == "POST":
        curr_entered_pwd = request.form["password_current"]
        new_entered_pwd = request.form["password_new"]
        user_check = Users.query.filter_by(id=current_user.id).first()

        if sha256_crypt.verify(curr_entered_pwd, user_check.password):
            flash("Password changed successfully.")
            new_encrypted_password = sha256_crypt.hash(new_entered_pwd)
            user_check.password = new_encrypted_password
            db.session.commit()
        else:
            flash("Your current password was entered incorrectly. Try again.")
        return render_template('account.html',
                               update_password_form=update_password_form)


# Logout users
@auth_bp.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.")
    return redirect(url_for('main_bp.index'))


# Sign up new users
@auth_bp.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    sign_up_form = SignUpForm()
    if request.method == "GET":
        return render_template('sign_up.html', sign_up_form=sign_up_form)
    elif request.method == "POST":
        username_flask = (request.form['username']).lower()
        password_flask = request.form['password']
        encrypted_password = sha256_crypt.hash(password_flask)

        user_check = Users.query.filter_by(username=username_flask).first()
        if user_check:
            flash("Username is taken. Please enter another one.")
            return redirect(url_for('auth_bp.sign_up'))

        new_user = Users(username=username_flask, password=encrypted_password)

    # add the new user to the database
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth_bp.login'))
        except:
            flash("There was an error in the sign up process. Please try again later.")
            return redirect(url_for('main_bp.index'))