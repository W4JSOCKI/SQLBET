from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Kursy
from . import db
from .models import Admin,Mecz,Klient,Kursy,Kupon,Zaklad,Portfel
from sqlalchemy import select, update, insert, delete,distinct,between
import json

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
    return render_template("historia.html", user=current_user,kupony=kupony,type=0)
