from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Admin
from werkzeug.security import generate_password_hash
from . import db
from files.Ligi_zespoly import *
from flask_login import current_user


dod_admin = Blueprint('dod_admin', __name__)

@dod_admin.route('/dodadmin', methods=['GET', 'POST'])
def dodaj_admina():
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


@dod_admin.route('/dodmecz', methods=['GET', 'POST'])
def dodaj_mecz():
    if request.method == 'POST':
        data = request.form.get('data')
        liga = request.form.get('liga')
        druzyna1 = request.form.get('druzyna1')
        druzyna2 = request.form.get('druzyna2')
        wynik = request.form.get('wynik')

        if(druzyna2 == druzyna1):
            flash("You can't have same teams against each other...", category = "error")

        elif data == None:
            flash("You have to chose a date", category='error')
        else:



            print(data, liga, druzyna1, druzyna2)
    return render_template("New_game.html", user=current_user,Ligi=Ligi)
