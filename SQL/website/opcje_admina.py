from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Admin,Mecz,Klient
from werkzeug.security import generate_password_hash
from . import db
from SQL.files.Ligi_zespoly import *
from sqlalchemy import select, update, insert, delete
from flask_login import current_user
from datetime import datetime,date


dod_admin = Blueprint('dod_admin', __name__)

@dod_admin.route('/dodadmin', methods=['GET', 'POST'])
def dodaj_admina():
    if request.method == 'POST':
        email = request.form.get('email')
        level = request.form.get('level', type=int)
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        sql=select(Klient.email)
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


@dod_admin.route('/dodmecz', methods=['GET', 'POST'])
def dodaj_mecz():
    if request.method == 'POST':
        conn = db.engine.connect()
        data = request.form.get('data')
        liga = request.form.get('liga')
        druzyna1 = request.form.get('druzyna1')
        druzyna2 = request.form.get('druzyna2')

        if (data == None):
            flash("You have to chose a date", category='error')
        elif(druzyna1 == None or druzyna2 == None):
            flash("You must select teams",category='error')
        elif (druzyna2 == druzyna1) :
            flash("You can't have same teams against each other...", category = "error")

        else:
            data = str(data).split('-')
            print(data, liga, druzyna1, druzyna2)
            sql = insert(Mecz).values(data_meczu=datetime(int(data[0]),int(data[1]),int(data[2])), liga=liga, dr1=druzyna1,dr2=druzyna2)
            conn.execute(sql)
            return redirect(url_for('views.home_admin'))

    return render_template("New_game.html", user=current_user,Ligi=Ligi)

@dod_admin.route('/zmmecz', methods=['GET', 'POST'])
def edytuj_mecz():
    if request.method == 'GET':
        conn = db.engine.connect()
        sql = select(Mecz.id_meczu,Mecz.liga,Mecz.data_meczu, Mecz.dr1, Mecz.dr2)
        ligi = conn.execute(sql).fetchall()

    if request.method == 'POST':
      #  game = request.form.get('game')
      #  if (game == None):
         #   flash("You have to chose a game", category='error')
       # else:
           # data = str(data).split('-')
          #  print(game)
           # sql = insert(Mecz).values(data_meczu=datetime(int(data[0]),int(data[1]),int(data[2])), liga=liga, dr1=druzyna1,dr2=druzyna2)
            #conn.execute(sql)
            return redirect(url_for('dod_admin.update_mecz'))

    return render_template("edit_game.html", user=current_user,Ligi=ligi)


@dod_admin.route('/updateecz', methods=['GET', 'POST'])
def update_mecz(): #nie dziala dobrze
    x=0
    conn = db.engine.connect()
    if request.form == 'POST' or x == 0:
        id = request.form["game"]
        print(id)
        x=x+1
    if request.method == 'POST' and x == 1:

        data = request.form.get('data')
        liga = request.form.get('liga')
        druzyna1 = request.form.get('druzyna1')
        druzyna2 = request.form.get('druzyna2')

        if (data == None):
            flash("You have to chose a date", category='error')
        elif(druzyna1 == None or druzyna2 == None):
            flash("You must select teams",category='error')
        elif (druzyna2 == druzyna1) :
            flash("You can't have same teams against each other...", category = "error")

        else:
            data = str(data).split('-')
            print(data, liga, druzyna1, druzyna2)
            sql = update(Mecz).values(data_meczu=datetime(int(data[0]),int(data[1]),int(data[2])), liga=liga, dr1=druzyna1,dr2=druzyna2).where()
            conn.execute(sql)
            x=0
            return redirect(url_for('views.home_admin'))

    return render_template("update_game.html", user=current_user,Ligi=Ligi)

