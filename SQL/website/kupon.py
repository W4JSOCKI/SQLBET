from flask import Blueprint, render_template, request, flash, redirect, url_for,Flask,request
from flask_login import login_required, current_user
from .models import Admin,Mecz,Klient,Kursy,Kupon,Zaklad,Portfel,Wplata,Wyplata
from . import db
from files.Ligi_zespoly import *
from sqlalchemy import select, update, insert, delete,distinct,between
from flask_login import current_user
from datetime import datetime,date,timedelta
import ast

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

    conn = db.engine.connect()
    if request.method=='POST':
        
        
        sql= select(Mecz.data_meczu, Mecz.dr1, Mecz.dr2,Mecz.wynik_meczu,Mecz.id_meczu)
        flaga=0
        kursy=[]
        mecze = conn.execute(sql).fetchall()
        meczeid=[]
        druzyny=[]
        daty=[]
        for mecz in mecze:
            i=request.form.get(str(mecz[4]))
           
            if(i in ["1","X","2"]):
                meczeid.append(mecz[4])
                druzyny.append([mecz[1],mecz[2]])
                daty.append(mecz[0])
                flaga=1
                sql=select(Kursy.id_kursu,Kursy.kurs1,Kursy.kursx,Kursy.kurs2).where(Kursy.Mecz_id_meczu==mecz[4]).order_by(Kursy.data.desc()).limit(1)
                id_kursy=conn.execute(sql).fetchone()
                if(i=="1"):
                    kursy.append([id_kursy[1],"1"])
                elif(i=="X"):
                    kursy.append([id_kursy[2], "X"])
                else:
                    kursy.append([id_kursy[3], "2"])
            
        if(flaga==0):
            flash("Nie wybrałeś żadnego meczu",category='error')
            return redirect(url_for('kupony.home'))
        else: 
            finalkurs=1
            for kurs in kursy:
                finalkurs=finalkurs*kurs[0]

    sql = select(Portfel.id_portfela,Portfel.id_klienta,Portfel.stan).where(Portfel.id_klienta==current_user.id_user)
    
    portfele = conn.execute(sql).fetchall()
    maxdata=max(daty)
    button_tags=[]
    for i in range(1,len(portfele)+1):
        button_tags.append("Portfel "+str(i))        
           
        
    return render_template("nowy_kupon.html",user=current_user,meczeid=meczeid,kursy=kursy,finalkurs=finalkurs
    ,druzyny=druzyny,daty=daty,type=0,portfeles=button_tags,maxdata=maxdata)

        
@kupony.route('/historia_kuponów', methods=['GET', 'POST'])
@login_required
def kupony_historia():


    conn = db.engine.connect()
    if(request.method=='POST'):
        
        finalkurs=float(request.form.get('kurs'))
        meczeid=request.form.get('meczeid')
        pdata=request.form.get('data')
        pdata = str(pdata).split('-')
        enddate = datetime(int(pdata[0]), int(pdata[1]), int(pdata[2]))
        portfel=request.form.get('portfel')
        kwota=float(request.form.get('kwota'))
        kursy=request.form.get('kursy')
        
        original_list = ast.literal_eval(kursy)
        kursy = [[float(i[0]), i[1]] for i in original_list]
        original_list = ast.literal_eval(meczeid)
        meczeid = [int(i) for i in original_list]
        print(kursy[0])

        sql=select(Portfel.id_portfela,Portfel.id_klienta,Portfel.stan).where(Portfel.id_klienta==current_user.id_user)
        portfele = conn.execute(sql).fetchall()
        pn=int(portfel[-1])
        pid=portfele[pn-1][0]
        if(portfele[pn-1][2]<kwota):
            flash("Za mało środków na koncie",category='error')
            return redirect(url_for('mecze.home'))
        potencjalna_wygrana=kwota*finalkurs
        sql=insert(Kupon).values(Klient_id_user=current_user.id_user,data_zakonczenia=enddate,kwota=kwota,kurs=finalkurs,
        potencjalna_wygrana=potencjalna_wygrana, stan="Dodany")
        conn.execute(sql)
        sql=select(Kupon.id_kuponu).where(Kupon.Klient_id_user==current_user.id_user).order_by(Kupon.id_kuponu.desc()).limit(1)
        id_kuponu=conn.execute(sql).fetchone()
        for i in range(0,len(meczeid)):
            sql=insert(Zaklad).values(Kupon_id_kuponu=id_kuponu[0],kurs=float(kursy[i][0]),Mecz_id_meczu=meczeid[i],typ=kursy[i][1],stan="Aktywny")
            conn.execute(sql)
        
        
    sql=update(Portfel).where(Portfel.id_portfela==pid).values(stan=Portfel.stan-kwota)
    conn.execute(sql)
    sql=insert(Wyplata).values(Portfel_id_portfela=pid,kwota=kwota,czy_z_kuponu='T')
    conn.execute(sql)
 
    sql=select(Kupon.id_kuponu,Kupon.data_zakonczenia,Kupon.kwota,Kupon.kurs,Kupon.potencjalna_wygrana,Kupon.stan).where(Kupon.Klient_id_user==current_user.id_user).order_by(Kupon.id_kuponu.desc())
    kupon = conn.execute(sql).fetchone()
    print(kupon)
    print(kupon[2])
    z1="{:.2f}".format(kupon[2])
    z2="{:.2f}".format(kupon[3])
    z3="{:.2f}".format(kupon[4])
    kupon=[kupon[0],kupon[1],z1,z2,z3,kupon[5]]


    return render_template("historia_kuponów.html",user=current_user,type=0,coupon=kupon)


