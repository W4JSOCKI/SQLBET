from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Admin,Mecz,Klient
from . import db
from files.Ligi_zespoly import *
from sqlalchemy import select, update, insert, delete,distinct
from flask_login import current_user
from datetime import datetime,date

mecze = Blueprint('mecze', __name__)


@mecze.route('/mecze', methods=['GET', 'POST'])
@login_required
def home():
    
    conn = db.engine.connect()
    if request.method=='POST':
        liga=request.form.getlist('liga')
        sql=select(Mecz.data_meczu, Mecz.dr1, Mecz.dr2,Mecz.wynik_meczu).where(Mecz.liga==liga[0])
        mecze = conn.execute(sql).fetchall()
    else:
        sql = select(Mecz.data_meczu, Mecz.dr1, Mecz.dr2,Mecz.wynik_meczu)
        mecze = conn.execute(sql).fetchall()
    
   
    sql = select(Mecz.liga).distinct()
    ligi = conn.execute(sql).fetchall()
    return render_template("mecze.html", user=current_user, type = 0,matches=mecze,Ligi=ligi)

