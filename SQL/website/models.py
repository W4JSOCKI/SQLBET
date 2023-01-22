from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Uzytkownik(db.Model,UserMixin):
    id_user = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    discriminator = db.Column('type', db.String(50))
    __mapper_args__ = {'polymorphic_on': discriminator}


class Admin(Uzytkownik):
    id = db.Column(None, db.ForeignKey('uzytkownik.id_user'), primary_key=True)
    poziom = db.Column(db.Integer)
    __mapper_args__ = {'polymorphic_identity': 'admin'}

class Klient(Uzytkownik):
    id = db.Column(None, db.ForeignKey('uzytkownik.id_user'), primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    __mapper_args__ = {'polymorphic_identity': 'klient'}


class Kursy(db.Model):
    kurs = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, default=func.today())
    Mecz_id_meczu = db.Column(db.Integer, db.ForeignKey('mecz.id_meczu'))

class Mecz(db.Model):
    id_meczu = db.Column(db.Integer, primary_key=True)
    data_meczu = db.Column(db.Date, default=func.today())
    liga = db.Column(db.String(100))
    dr1 = db.Column(db.String(80))
    dr2 = db.Column(db.String(80))
    wynik_meczu = db.Column(db.String(1))
    kurs = db.relationship('Kursy')
    zaklad = db.relationship('Zaklad')

class Zaklad(db.Model):
    id_zakladu = db.Column(db.Integer, primary_key=True)
    kurs = db.Column(db.Float)
    typ = db.Column(db.String(1))
    Kupon_id_kuponu = db.Column(db.Integer, db.ForeignKey('kupon.id_kuponu'))
    Mecz_id_meczu = db.Column(db.Integer, db.ForeignKey('mecz.id_meczu'))

class Kupon(db.Model):
    id_kuponu = db.Column(db.Integer, primary_key=True)
    data_zakonczenia = db.Column(db.Date, default=func.today())
    kwota = db.Column(db.Integer)
    kurs = db.Column(db.Float)
    potencjalna_wygrana = db.Column(db.Float)
    stan = db.Column(db.String(20))
    Klient_id_user = db.Column(db.Integer, db.ForeignKey('klient.id_user'))

class Portfel(db.Model):
    id_portfela = db.Column(db.Integer, primary_key=True)
    id_klienta = db.Column(db.Integer)
    stan = db.Column(db.Float)
    Klient_id_user = db.Column(db.Integer, db.ForeignKey('klient.id_user'))
    zaklad = db.relationship('Wplata')
    zaklad = db.relationship('Wyplata')

class Wplata(db.Model):
    id_wplaty = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, default=func.today())
    kwota = db.Column(db.Float)
    czy_z_kuponu = db.Column(db.String(1))
    Portfel_id_portfela = db.Column(db.Integer, db.ForeignKey('portfel.id_portfela'))


class Wyplata(db.Model):
    id_wypłaty = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, default=func.today())
    kwota = db.Column(db.Float)
    czy_z_kuponu = db.Column(db.String(1))
    Portfel_id_portfela = db.Column(db.Integer, db.ForeignKey('portfel.id_portfela'))

    
