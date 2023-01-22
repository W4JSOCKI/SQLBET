from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Admin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from sqlalchemy import select
from flask_login import login_user, login_required, logout_user, current_user


auth_admin = Blueprint('auth_admin', __name__)


@auth_admin.route('/login-admin', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = Admin.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home_admin'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('You are not an admin.', category='error')

    return render_template("login.html", user=current_user)


@auth_admin.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_admin.login'))


