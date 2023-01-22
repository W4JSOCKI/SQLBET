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
    conn = db.engine.connect()
    portfele = conn.execute(sql).fetchall()

    button_tags=[]
    for i in range(1,len(portfele)+1):
        button_tags.append("Portfel"+str(i))
    
    pages_tags = ["/portfel1","/portfel2","/portfel3"]
    #TODO - redirect to wallets after clicking on buttons
    #button_tags =["Portfel #1","Portfel #2"]

    return render_template("portfel.html", user=current_user,button_tags=button_tags)

@portfel.route('/portfel1', methods=['GET', 'POST'])
@login_required
def portfel1():
    pn="Portfel #1"
    return render_template("portfel1.html", user=current_user, pn=pn)



@portfel.route('/portfel2', methods=['GET', 'POST'])
@login_required
def portfel2():
    pn="Portfel #2"
    return render_template("portfel1.html", user=current_user,  pn=pn)



@portfel.route('/portfel3', methods=['GET', 'POST'])
@login_required
def portfel3():
    pn="Portfel #3"
    return render_template("portfel1.html", user=current_user,  pn=pn)
