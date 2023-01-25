from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Admin,Mecz,Klient
from . import db
from files.Ligi_zespoly import *
from sqlalchemy import select, update, insert, delete,distinct,between
from flask_login import current_user
from datetime import datetime,date

mecze = Blueprint('mecze', __name__)


@mecze.route('/mecze', methods=['GET', 'POST'])
@login_required
def home():
    
    conn = db.engine.connect()
    if request.method=='POST':
        ligat=request.form.getlist('liga')
        mindate = request.form.get('match-date-min')
        maxdate = request.form.get('match-date-max')
        if(ligat[0]=="Wszystkie Ligi"):
            sql=select(Mecz.data_meczu, Mecz.dr1, Mecz.dr2,Mecz.wynik_meczu).where(Mecz.data_meczu.between(mindate,maxdate))
        else:
            sql=select(Mecz.data_meczu, Mecz.dr1, Mecz.dr2,Mecz.wynik_meczu).where(Mecz.liga==ligat[0], Mecz.data_meczu.between(mindate,maxdate))
        
        mecze = conn.execute(sql).fetchall()
        liga=ligat[0]
        
    else:
        sql = select(Mecz.data_meczu, Mecz.dr1, Mecz.dr2,Mecz.wynik_meczu)
        mecze = conn.execute(sql).fetchall()
        mindate="2000-01-01"
        maxdate="2050-12-31"
        liga="Wszystkie Ligi"
    
    
   
    sql = select(Mecz.liga).distinct()
    ligi = conn.execute(sql).fetchall()
    
    return render_template("mecze.html", user=current_user, type = 0,matches=mecze,Ligi=ligi,cliga=liga,mdatemin=mindate,mdatemax=maxdate)

