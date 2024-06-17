from application import app
from application.forms import *
from application.models import *
from flask import render_template, request, flash, redirect, json, jsonify, url_for, make_response, send_file
from flask_login import login_user, login_required, current_user, logout_user, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash

#Handles http://127.0.0.1:5000/
@app.route('/') 
def index():
    return render_template('index.html')

# Page route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Retrieve the form 
    form = loginForm()

    # Check if the user is trying to login
    if request.method == 'POST':
        # Retrieve the username from the form sent
        username = form.username.data
        # Retrieve the password from the form sent
        password = form.password.data

        # Query the User table to see if the username is in the database
        user = User.query.filter_by(username = username).first()
        
        # Check if the user credentials are wrong
        # By checking if the userexists and if the password submitted matches the user's password in the database
        if not user or not check_password_hash(user.password, password):
            # Refresh the page and display an error message if the credentials are incorrect
            flash('Please check your login details and try again', 'warning')
            return redirect(url_for('login'))
        # If the credentials are correct we login the user and direct them to the home page
        login_user(user)
        return redirect(url_for('index'))
    # Loads the login page
    return render_template("login.html", form = form, title = 'Login')

# Page route for the register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Retrieve the register form
    form = registerForm()
    if request.method == 'POST':
        # Retrieve the username from the form sent
        username = form.username.data
        # Retrieve the email from the form sent
        email = form.email.data
        # Retrieve the password from the form sent
        password = form.password.data
        # Retrieve the confirmation password from the form sent
        confirm = form.confirm.data

        # Check if the form is filled up correctly
        if form.validate_on_submit():
            # Check if the username submitted already exists in the database
            user = User.query.filter_by(username = username).first()

            if user:
                # If the username already exists in the database we refresh the page and display an error message
                flash('Username already exists', 'warning')
                return redirect(url_for('login'))
            
            # Create a new user in the database
            new_user = User(username = username, email = email, password = generate_password_hash(password, method='sha256'))

            db.session.add(new_user)
            db.session.commit()

            # Direct the user to the login page and display a success message
            flash(f"Registration: success", "success")
            return redirect(url_for('login'))
        else: 
            # If the two passwords are not the same we refresh the page with an error message
            if password != confirm:
                flash("Both passwords must match!", "warning")
                return redirect(url_for('register'))

            else:
                # Refresh the page and display an error message
                flash("Account could not be created, please check your credentials and try again.", 'danger')
                return redirect(url_for('register'))
    # Loads the register page
    return render_template("register.html", form = form, title = 'Register')