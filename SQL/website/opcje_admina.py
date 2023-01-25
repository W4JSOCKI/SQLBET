from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Admin, Mecz, Klient, Kursy
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
        elif (data == ""):
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
            flash("Game added", category="success")
            return redirect(url_for('views.home_admin'))

    return render_template("New_game.html", user=current_user,Ligi=Ligi)

@dod_admin.route('/zmmecz', methods=['GET', 'POST'])
def edytuj_mecz():
    conn = db.engine.connect()
    sql = select(Mecz.id_meczu, Mecz.liga, Mecz.data_meczu, Mecz.dr1, Mecz.dr2)
    ligi = conn.execute(sql).fetchall()
    if request.method == 'POST':

        id = request.form.get("game")
        data = request.form.get('data')
        liga = request.form.get('liga')
        druzyna1 = request.form.get('druzyna1')
        druzyna2 = request.form.get('druzyna2')
        print(id, data, liga, druzyna1, druzyna2)

        if (data == None):
            flash("You have to chose a date", category='error')
        elif (druzyna1 == None or druzyna2 == None):
            flash("You must select teams", category='error')
        elif (druzyna2 == druzyna1):
            flash("You can't have same teams against each other...", category="error")

        else:
            conn = db.engine.connect()
            data = str(data).split('-')
            print(data, liga, druzyna1, druzyna2)
            sql = update(Mecz).values(data_meczu=datetime(int(data[0]), int(data[1]), int(data[2])), liga=liga,
                                      dr1=druzyna1, dr2=druzyna2).where(Mecz.id_meczu == id)
            conn.execute(sql)
            print(id,data,liga,druzyna1,druzyna2)
            flash("Game changed", category="success")
            return redirect(url_for('views.home_admin'))

    return render_template("edit_game.html", user=current_user,Ligi=Ligi,Mecze=ligi)


@dod_admin.route('/zmwynik', methods=['GET', 'POST'])
def dodaj_wynik():
    conn = db.engine.connect()
    sql = select(Mecz.id_meczu, Mecz.liga, Mecz.data_meczu, Mecz.dr1, Mecz.dr2)
    alll = conn.execute(sql).fetchall()
    if request.method == 'POST':

        id = request.form.get("game")
        gole1 = request.form.get('gole1',type=int)
        gole2 = request.form.get('gole2',type= int)
        wynik = 'X'
        print(id, gole2, gole1)
        if (gole2 == None or gole1 == None):
            flash("You have to chose a date", category='error')

        else:
            conn = db.engine.connect()
            if gole2>gole1:
                print(gole2)
                wynik='2'

            elif gole1>gole2:
                print(gole1)
                wynik='1'

            else:
                wynik='X'

            sql = update(Mecz).where(Mecz.id_meczu==id).values(wynik_meczu=wynik)
            conn.execute(sql)

            return redirect(url_for('views.home_admin'))

    return render_template("dod_wynik.html", user=current_user,Mecze=alll)


@dod_admin.route('/dodkurs', methods=['GET', 'POST'])
def dodaj_kurs():
    conn = db.engine.connect()
    sql = select(Mecz.id_meczu, Mecz.liga, Mecz.data_meczu, Mecz.dr1, Mecz.dr2)
    alll = conn.execute(sql).fetchall()
    if request.method == 'POST':

        kurs1 = request.form.get("kurs1")
        kurs2 = request.form.get("kurs2")
        kursx = request.form.get("kursx")
        data = date.today()
        #data=datetime.now()
        id_meczu = request.form.get("game")
        print(kurs1,kursx,kurs2,data,id_meczu)
        if id_meczu == None:
            flash("Musisz Wybrac mecz!",category='error')
        else:
            flash("Succes: Kurs dodany! ",category='success')
            #sql= insert(Kursy).values(kurs1=kurs1,kurs2=kurs2,kursx=kursx,data=data,Mecz_id_meczu=id_meczu)
            #conn.execute(sql)
            return redirect(url_for('views.home_admin'))

    return render_template("dod_kurs.html", user=current_user,Mecze=alll)


