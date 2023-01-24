from flask import Blueprint, render_template, request, flash, jsonify,redirect,url_for
from flask_login import login_required, current_user
from .models import Portfel, Wplata, Wyplata
from sqlalchemy import select, update, insert, delete,event
from . import db
import json
import numpy as np
from datetime import date



portfel = Blueprint('portfel', __name__)

@event.listens_for(Portfel, "before_delete")
def receive_before_delete(mapper, connection, target):
    for child in target.children:
        connection.delete(child)


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
    
    
    #TODO - redirect to wallets after clicking on buttons
    #button_tags =["Portfel #1","Portfel #2"]

    return render_template("portfel.html", user=current_user,button_tags=button_tags,type=0)

@portfel.route('/deletep', methods=['DELETE'])
def deletep():
    data = request.get_json()
    record_id = int(data["id"])
    userid=current_user.id_user
    sql = select(Portfel.id_portfela).where(Portfel.id_klienta==userid).order_by(Portfel.id_portfela)
    conn = db.engine.connect()
    portfele = conn.execute(sql).fetchall()
    port_id=portfele[1][0]
    child_sql = delete(Wplata).where(Wplata.Portfel_id_portfela == port_id)
    conn.execute(child_sql)
    child_sql = delete(Wyplata).where(Wyplata.Portfel_id_portfela == port_id)
    conn.execute(child_sql)
   
    
    sql= (delete(Portfel).where(Portfel.id_portfela==port_id))
    result = conn.execute(sql)


    

    return jsonify({"status": "ok"},200) 

@portfel.route('/addp')
def addp():
    
    userid=current_user.id_user
    conn = db.engine.connect()

    sql = insert(Portfel).values(id_klienta=userid,stan=0)
    result = conn.execute(sql)
    return redirect(url_for('portfel.home'))
    

@portfel.route('/portfel1', methods=['GET', 'POST'])
@login_required
def portfel1():
    pn="Portfel #1"
    sql = select(Portfel.id_portfela,Portfel.stan).where(Portfel.id_klienta==current_user.id_user)
    conn = db.engine.connect()
    portfele = conn.execute(sql).first()
    stan=float(portfele[1])
    sql = select(Wplata.id_wplaty,Wplata.data,Wplata.kwota,Wplata.czy_z_kuponu).where(Wplata.Portfel_id_portfela==portfele[0]).order_by(Wplata.data.desc(),Wplata.id_wplaty.desc())
    wplaty = conn.execute(sql).fetchall()
    sql = select(Wyplata.id_wypłaty,Wyplata.data,Wyplata.kwota,Wyplata.czy_z_kuponu).where(Wyplata.Portfel_id_portfela==portfele[0]).order_by(Wyplata.data.desc(),Wyplata.id_wypłaty.desc())
    wyplaty = conn.execute(sql).fetchall() 
    if request.method == "POST":
        deposit = request.form["deposit"]
        if(len(deposit)>0):
            fdeposit=float(deposit)
        payoff = request.form["payoff"]
        if(len(payoff)>0):
            fpayoff=float(payoff)
        
        if(len(deposit)>0 and len(payoff)>0):
            if (stan+fdeposit-fpayoff)<0:
                flash("Nie możesz tego zrobić, po tej operacji saldo będzie ujemne", category="error")
            else:
                stan=stan+fdeposit-fpayoff
                sql =( update(Portfel).where(Portfel.id_portfela==portfele[0]).values(stan=stan))
                conn.execute(sql)
                today=date.today()
                sql = insert(Wplata).values(Portfel_id_portfela=portfele[0],kwota=fdeposit,czy_z_kuponu='T',data=today)
                conn.execute(sql)
                sql = insert(Wyplata).values(Portfel_id_portfela=portfele[0],kwota=fpayoff,czy_z_kuponu='T',data=today)
                conn.execute(sql)
                flash("Operacja zrealizowana pomyślnie", category="success") 
        elif(len(deposit)>0):
            stan=stan+fdeposit
            sql =( update(Portfel).where(Portfel.id_portfela==portfele[0]).values(stan=stan))
            conn.execute(sql)
            today=date.today()
            sql = insert(Wplata).values(Portfel_id_portfela=portfele[0],kwota=fdeposit,czy_z_kuponu='T',data=today)
            conn.execute(sql)
            flash("Operacja zrealizowana pomyślnie", category="success")
        elif(len(payoff)>0):
            if (stan-fpayoff)<0:
                flash("Nie możesz tego zrobić, po tej operacji saldo będzie ujemne", category="error")
            else:
                stan=stan-fpayoff
                sql =( update(Portfel).where(Portfel.id_portfela==portfele[0]).values(stan=stan))
                conn.execute(sql)
                today=date.today()
                sql = insert(Wyplata).values(Portfel_id_portfela=portfele[0],kwota=fpayoff,czy_z_kuponu='T',data=today)
                conn.execute(sql)
                flash("Operacja zrealizowana pomyślnie", category="success")
        
        

    sql = select(Portfel.id_portfela,Portfel.stan).where(Portfel.id_klienta==current_user.id_user)
    conn = db.engine.connect()
    portfele = conn.execute(sql).first()
    stan=float(portfele[1])
    sql = select(Wplata.id_wplaty,Wplata.data,Wplata.kwota,Wplata.czy_z_kuponu).where(Wplata.Portfel_id_portfela==portfele[0]).order_by(Wplata.data.desc(),Wplata.id_wplaty.desc())
    wplaty = conn.execute(sql).fetchall()
    sql = select(Wyplata.id_wypłaty,Wyplata.data,Wyplata.kwota,Wyplata.czy_z_kuponu).where(Wyplata.Portfel_id_portfela==portfele[0]).order_by(Wyplata.data.desc(),Wyplata.id_wypłaty.desc())
    wyplaty = conn.execute(sql).fetchall() 
    stan="{:.2f}".format(stan)
    ptag="/portfel1"
    return render_template("portfel1.html", user=current_user, pn=pn, payments=wplaty, payoffs=wyplaty,stan=stan,ptag=ptag,type=0)



@portfel.route('/portfel2', methods=['GET', 'POST'])
@login_required
def portfel2():
    pn="Portfel #2"
    sql = select(Portfel.id_portfela,Portfel.stan).where(Portfel.id_klienta==current_user.id_user)
    conn = db.engine.connect()
    portfele = conn.execute(sql).fetchall()
    stan=float(portfele[1][1])
    sql = select(Wplata.id_wplaty,Wplata.data,Wplata.kwota,Wplata.czy_z_kuponu).where(Wplata.Portfel_id_portfela==portfele[1][0]).order_by(Wplata.data.desc(),Wplata.id_wplaty.desc())
    wplaty = conn.execute(sql).fetchall()
    sql = select(Wyplata.id_wypłaty,Wyplata.data,Wyplata.kwota,Wyplata.czy_z_kuponu).where(Wyplata.Portfel_id_portfela==portfele[1][0]).order_by(Wyplata.data.desc(),Wyplata.id_wypłaty.desc())
    wyplaty = conn.execute(sql).fetchall() 
    if request.method == "POST":
        deposit = request.form["deposit"]
        if(len(deposit)>0):
            fdeposit=float(deposit)
        payoff = request.form["payoff"]
        if(len(payoff)>0):
            fpayoff=float(payoff)
        
        if(len(deposit)>0 and len(payoff)>0):
            if (stan+fdeposit-fpayoff)<0:
                flash("Nie możesz tego zrobić, po tej operacji saldo będzie ujemne", category="error")
            else:
                stan=stan+fdeposit-fpayoff
                sql =( update(Portfel).where(Portfel.id_portfela==portfele[1][0]).values(stan=stan))
                conn.execute(sql)
                today=date.today()
                sql = insert(Wplata).values(Portfel_id_portfela=portfele[1][0],kwota=fdeposit,czy_z_kuponu='T',data=today)
                conn.execute(sql)
                sql = insert(Wyplata).values(Portfel_id_portfela=portfele[1][0],kwota=fpayoff,czy_z_kuponu='T',data=today)
                conn.execute(sql)
                flash("Operacja zrealizowana pomyślnie", category="success") 
        elif(len(deposit)>0):
            stan=stan+fdeposit
            sql =( update(Portfel).where(Portfel.id_portfela==portfele[1][0]).values(stan=stan))
            conn.execute(sql)
            today=date.today()
            sql = insert(Wplata).values(Portfel_id_portfela=portfele[1][0],kwota=fdeposit,czy_z_kuponu='T',data=today)
            conn.execute(sql)
            flash("Operacja zrealizowana pomyślnie", category="success")
        elif(len(payoff)>0):
            if (stan-fpayoff)<0:
                flash("Nie możesz tego zrobić, po tej operacji saldo będzie ujemne", category="error")
            else:
                stan=stan-fpayoff
                sql =( update(Portfel).where(Portfel.id_portfela==portfele[1][0]).values(stan=stan))
                conn.execute(sql)
                today=date.today()
                sql = insert(Wyplata).values(Portfel_id_portfela=portfele[1][0],kwota=fpayoff,czy_z_kuponu='T',data=today)
                conn.execute(sql)
                flash("Operacja zrealizowana pomyślnie", category="success")
        

    sql = select(Portfel.id_portfela,Portfel.stan).where(Portfel.id_klienta==current_user.id_user)
    conn = db.engine.connect()
    portfele = conn.execute(sql).fetchall()
    stan=float(portfele[1][1])
    sql = select(Wplata.id_wplaty,Wplata.data,Wplata.kwota,Wplata.czy_z_kuponu).where(Wplata.Portfel_id_portfela==portfele[1][0]).order_by(Wplata.data.desc(),Wplata.id_wplaty.desc())
    wplaty = conn.execute(sql).fetchall()
    sql = select(Wyplata.id_wypłaty,Wyplata.data,Wyplata.kwota,Wyplata.czy_z_kuponu).where(Wyplata.Portfel_id_portfela==portfele[1][0]).order_by(Wyplata.data.desc(),Wyplata.id_wypłaty.desc())
    wyplaty = conn.execute(sql).fetchall() 
    stan="{:.2f}".format(stan)

    ptag="/portfel2"
    
    return render_template("portfel1.html", user=current_user, pn=pn, payments=wplaty, payoffs=wyplaty,stan=stan,ptag=ptag,type=0)



@portfel.route('/portfel3', methods=['GET', 'POST'])
@login_required
def portfel3():
    pn="Portfel #3"
    sql = select(Portfel.id_portfela,Portfel.stan).where(Portfel.id_klienta==current_user.id_user)
    conn = db.engine.connect()
    portfele = conn.execute(sql).fetchall()
    stan=float(portfele[2][1])
    sql = select(Wplata.id_wplaty,Wplata.data,Wplata.kwota,Wplata.czy_z_kuponu).where(Wplata.Portfel_id_portfela==portfele[2][0]).order_by(Wplata.data.desc(),Wplata.id_wplaty.desc())
    wplaty = conn.execute(sql).fetchall()
    sql = select(Wyplata.id_wypłaty,Wyplata.data,Wyplata.kwota,Wyplata.czy_z_kuponu).where(Wyplata.Portfel_id_portfela==portfele[2][0]).order_by(Wyplata.data.desc(),Wyplata.id_wypłaty.desc())
    wyplaty = conn.execute(sql).fetchall() 
    if request.method == "POST":
        deposit = request.form["deposit"]
        if(len(deposit)>0):
            fdeposit=float(deposit)
        payoff = request.form["payoff"]
        if(len(payoff)>0):
            fpayoff=float(payoff)
        
        if(len(deposit)>0 and len(payoff)>0):
            if (stan+fdeposit-fpayoff)<0:
                flash("Nie możesz tego zrobić, po tej operacji saldo będzie ujemne", category="error")
            else:
                stan=stan+fdeposit-fpayoff
                sql =( update(Portfel).where(Portfel.id_portfela==portfele[2][0]).values(stan=stan))
                conn.execute(sql)
                today=date.today()
                sql = insert(Wplata).values(Portfel_id_portfela=portfele[2][0],kwota=fdeposit,czy_z_kuponu='T',data=today)
                conn.execute(sql)
                sql = insert(Wyplata).values(Portfel_id_portfela=portfele[2][0],kwota=fpayoff,czy_z_kuponu='T',data=today)
                conn.execute(sql)
                flash("Operacja zrealizowana pomyślnie", category="success") 
        elif(len(deposit)>0):
            stan=stan+fdeposit
            sql =( update(Portfel).where(Portfel.id_portfela==portfele[2][0]).values(stan=stan))
            conn.execute(sql)
            today=date.today()
            sql = insert(Wplata).values(Portfel_id_portfela=portfele[2][0],kwota=fdeposit,czy_z_kuponu='T',data=today)
            conn.execute(sql)
            flash("Operacja zrealizowana pomyślnie", category="success")
        elif(len(payoff)>0):
            if (stan-fpayoff)<0:
                flash("Nie możesz tego zrobić, po tej operacji saldo będzie ujemne", category="error")
            else:
                stan=stan-fpayoff
                sql =( update(Portfel).where(Portfel.id_portfela==portfele[2][0]).values(stan=stan))
                conn.execute(sql)
                today=date.today()
                sql = insert(Wyplata).values(Portfel_id_portfela=portfele[2][0],kwota=fpayoff,czy_z_kuponu='T',data=today)
                conn.execute(sql)
                flash("Operacja zrealizowana pomyślnie", category="success")
        

    sql = select(Portfel.id_portfela,Portfel.stan).where(Portfel.id_klienta==current_user.id_user)
    conn = db.engine.connect()
    portfele = conn.execute(sql).fetchall()
    stan=float(portfele[2][1])
    sql = select(Wplata.id_wplaty,Wplata.data,Wplata.kwota,Wplata.czy_z_kuponu).where(Wplata.Portfel_id_portfela==portfele[2][0]).order_by(Wplata.data.desc(),Wplata.id_wplaty.desc())
    wplaty = conn.execute(sql).fetchall()
    sql = select(Wyplata.id_wypłaty,Wyplata.data,Wyplata.kwota,Wyplata.czy_z_kuponu).where(Wyplata.Portfel_id_portfela==portfele[2][0]).order_by(Wyplata.data.desc(),Wyplata.id_wypłaty.desc())
    wyplaty = conn.execute(sql).fetchall() 
    stan="{:.2f}".format(stan)

    ptag="/portfel3"
    return render_template("portfel1.html", user=current_user, pn=pn, payments=wplaty, payoffs=wyplaty,stan=stan,ptag=ptag,type=0)
