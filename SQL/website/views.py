from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Kursy
from . import db
from .models import Admin,Mecz,Klient,Kursy,Kupon,Zaklad,Portfel
from sqlalchemy import select, update, insert, delete,distinct,between
import json
from datetime import datetime,date

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    flash('Welcme to SQLBET!', category='success')

    return render_template("home.html", user=current_user, type = 0)

@views.route('/admin', methods=['GET', 'POST'])
def home_admin():
    return render_template("home_admin.html", user=current_user)

@views.route('/historia', methods=['GET', 'POST'])
def historia():
    conn = db.engine.connect()
    sql = select(Kupon.id_kuponu, Kupon.data_zakonczenia, Kupon.kwota, Kupon.kurs, Kupon.potencjalna_wygrana,
                 Kupon.stan).where(Kupon.Klient_id_user == current_user.id_user)
    kupony = conn.execute(sql).fetchall()
    #sql = select(Mecz.id_meczu, Mecz.data, Mecz.dr1, Mecz.dr2)

    for kupon in kupony:
        sql = select(Zaklad.id_zakladu, Zaklad.typ, Zaklad.kurs, Zaklad.Mecz_id_meczu).where(Zaklad.Kupon_id_kuponu == kupon.id_kuponu)
        zaklady = conn.execute(sql).fetchall()
        wyniki = []

        for zaklad in zaklady:
            print("ZALAD",zaklad)
            sql = select(Mecz.id_meczu, Mecz.wynik_meczu).where(Mecz.id_meczu == zaklad.Mecz_id_meczu)
            wyn = conn.execute(sql).fetchall()
            wyniki.append(wyn[0])

        if wyniki[0][1] == None:
            print(wyniki[0][1])
            if kupon.stan == "Dodany":
                stan = "Aktywny"
                sql = update(Kupon).where(Kupon.id_kuponu == kupon.id_kuponu).values(stan=stan)
                conn.execute(sql)
                return redirect(url_for('views.historia'))

            if kupon.stan == "Dodany":
                    stan = "Aktywny"
                    sql = update(Kupon).where(Kupon.id_kuponu == kupon.id_kuponu).values(stan=stan)
                    conn.execute(sql)
            if kupon.data_zakonczenia < datetime.date.today():
                #print(stan)
                #print(kupon.kurs,kupon.kwota,kupon.potencjalna_wygrana)

                if kupon.stan == "Aktywny":
                    print(kupon)
                elif kupon.stan == "Do odebrania":
                    stan = "Odebrany"
                    #sql = update(Kupon).where(Kupon.id_kuponu == kupon.id_kuponu).values(stan=stan)
                #conn.execute(sql)
                #print(kupon)
            #print(kupon)
    return render_template("historia.html", user=current_user,kupony=kupony,type=0)

@views.route('/usunsmecz', methods=['GET', 'POST'])
def usun_mecz():
    conn = db.engine.connect()
    sql = select(Mecz.id_meczu, Mecz.liga, Mecz.data_meczu, Mecz.dr1, Mecz.dr2,Mecz.wynik_meczu).where(Mecz.data_meczu > date.today(),Mecz.wynik_meczu == None).order_by(Mecz.data_meczu)
    ligi = conn.execute(sql).fetchall()

    if request.method == 'POST':
        id = request.form.get("game")
        sql = select(Kursy.id_kursu, Kursy.Mecz_id_meczu).where(Kursy.Mecz_id_meczu == id)
        kursy = conn.execute(sql).fetchall()
        emty = []
        if kursy != emty:
            print(kursy)
            flash('Nie można usunąć meczu, ponieważ istnieją kursy na ten mecz!', category='error')
            return redirect(url_for('views.home_admin'))
        else:


            sql = delete(Mecz).where(Mecz.id_meczu == id)
            conn.execute(sql)
            return redirect(url_for('views.home_admin'))

    return render_template("usun_mecz.html", user=current_user,Mecze=ligi,type=1)

