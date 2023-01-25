from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Admin, Klient
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
                login_user(user, remember=True)
                return redirect(url_for('views.home_admin'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('You are not an admin.', category='error')

        
    return render_template("login.html", user=current_user, type = 1)


@auth_admin.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_admin.login'))

@auth_admin.route('/sign-up-admin', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        level = request.form.get('level', type=int)
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        sql = select(Klient.email)
        conn = db.engine.connect()
        email_kli = conn.execute(sql)

        for i in email_kli:
            if email == i[0]:
                flash('Email already exists on client account.', category='error')
                return redirect(url_for('views.home_admin'))

        user = Admin.query.filter_by(email=email).first()

        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif type(level) != int:
            flash('Level is a number', category='error')
        elif level < 0 or level > 4:
            flash('Levels: 1-4', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = Admin(email=email, poziom=level, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('views.home_admin'))

    return render_template("sign_up_NEW_admin.html", user=current_user)


