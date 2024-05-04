from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from classes.class_user import User, LoginForm, RegisterForm
from app import db, bcrypt  # Import bcrypt from app

user_login_bp = Blueprint('user_login_bp', __name__)

@user_login_bp.route('/')
def home():
    return render_template('home.html')

@user_login_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('user_login_bp.dashboard'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('user_login_bp.login'))
    return render_template('login.html', form=form)

@user_login_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@user_login_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('user_login_bp.login'))

@user_login_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('user_login_bp.login'))
    return render_template('register.html', form=form)
