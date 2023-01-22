from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Portfel
from sqlalchemy import select
from . import db
import json

portfel = Blueprint('portfel', __name__)


@portfel.route('/portfel', methods=['GET', 'POST'])
@login_required
def home():
    #TODO - add button to add new wallet
    #TODO - take wallets from database
    sql = select(Portfel.id_portfela,Portfel.id_klienta,Portfel.stan).where(Portfel.id_klienta==current_user.id_user)
    print(sql)
    conn = db.engine.connect()
    portfele = conn.execute(sql).fetchall()
    print(portfele)


    #TODO - redirect to wallets after clicking on buttons
    button_tags =["Portfel #1","Portfel #2","Portfel #3"]

    return render_template("portfel.html", user=current_user,button_tags=button_tags)

