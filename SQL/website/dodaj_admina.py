from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Admin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


dod_admin = Blueprint('dod_admin', __name__)



@dod_admin.route('/dodadmin', methods=['GET', 'POST'])
def dodaj():
    if request.method == 'POST':
        email = request.form.get('email')
        level = request.form.get('level', type=int)
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = Admin.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif level <0 or level >4:
            flash('Levels: 0-4', category='error')
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

@dod_admin.route('/zmadmin', methods=['GET', 'POST'])
def edytuj():
    if request.method == 'POST':
        email = request.form.get('email')
        level = request.form.get('level', type=int)
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = Admin.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif level <0 or level >4:
            flash('Levels: 0-4', category='error')
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