from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Admin,Mecz,Klient,Kursy
from . import db
from files.Ligi_zespoly import *
from sqlalchemy import select, update, insert, delete,distinct,between
from flask_login import current_user
from datetime import datetime,date,timedelta

kupony = Blueprint('kupony', __name__)

@kupony.route('/makecoupon', methods=['GET', 'POST'])
@login_required
def home():
    
    conn = db.engine.connect()
    if request.method=='POST':
        ligat=request.form.getlist('liga')
        mindate = request.form.get('match-date-min')
        maxdate = request.form.get('match-date-max')
        if(ligat[0]=="Wszystkie Ligi"):
            sql=select(Mecz.data_meczu, Mecz.dr1, Mecz.dr2,Mecz.wynik_meczu,Mecz.id_meczu).where(Mecz.data_meczu.between(mindate,maxdate))
        else:
            sql=select(Mecz.data_meczu, Mecz.dr1, Mecz.dr2,Mecz.wynik_meczu,Mecz.id_meczu).where(Mecz.liga==ligat[0], Mecz.data_meczu.between(mindate,maxdate))
        
        mecze = conn.execute(sql).fetchall()
        liga=ligat[0]
        
    else:
        sql = select(Mecz.data_meczu, Mecz.dr1, Mecz.dr2,Mecz.wynik_meczu,Mecz.id_meczu).join(Kursy).where(Kursy.Mecz_id_meczu==Mecz.id_meczu).distinct()
       
        mecze = conn.execute(sql).fetchall()
        mindate=datetime.today()+timedelta(days=1)
        maxdate="2050-12-31"
        liga="Wszystkie Ligi"
    
    mindatehard=datetime.today()+timedelta(days=1)

    kursy=[]
    for mecz in mecze:
        sql=select(Kursy.kurs1,Kursy.kursx,Kursy.kurs2).where(Kursy.Mecz_id_meczu==mecz[4]).order_by(Kursy.data.desc()).limit(1)
       
        kursy.append(conn.execute(sql).fetchone())
    
    sql = select(Mecz.liga).distinct()
    ligi = conn.execute(sql).fetchall()
    
    return render_template("utworz_kupon.html", user=current_user, type = 0,matches=mecze,Ligi=ligi,cliga=liga,mdatemin=mindate,mdatemax=maxdate,mindatehard=mindatehard,kursy=kursy)

@kupony.route('/cupon', methods=['GET', 'post'])
@login_required
def coupon():

    print("a")
    if request.method=='POST':
        conn = db.engine.connect()
        print("b")
        sql= select(Mecz.data_meczu, Mecz.dr1, Mecz.dr2,Mecz.wynik_meczu,Mecz.id_meczu)
        mecze = conn.execute(sql).fetchall()
        for mecz in mecze:
            i=request.form.get(mecz[4])
            print(i)
       
    
    return redirect(url_for('kupony.home'))

        



