from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import event
from datetime import datetime

class Uzytkownik(db.Model,UserMixin):
    id_user = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    discriminator = db.Column('type', db.String(50))
    __mapper_args__ = {'polymorphic_on': discriminator}


class Admin(Uzytkownik):
    id = db.Column(None, db.ForeignKey('uzytkownik.id_user'), primary_key=True)
    poziom = db.Column(db.Integer, nullable=False)
    __mapper_args__ = {'polymorphic_identity': 'admin'}

class Klient(Uzytkownik):
    id = db.Column(None, db.ForeignKey('uzytkownik.id_user'), primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    kupon = db.relationship('Kupon')
    portfel = db.relationship('Portfel')
    __mapper_args__ = {'polymorphic_identity': 'klient'}


class Kursy(db.Model):
    id_kursu = db.Column(db.Integer, primary_key=True)
    kurs1 = db.Column(db.Integer, nullable=False)
    kurs2 = db.Column(db.Integer, nullable=False)
    kursx = db.Column(db.Integer, nullable=False)
    data = db.Column(db.Date, default=func.today(), nullable=False)
    Mecz_id_meczu = db.Column(db.Integer, db.ForeignKey('mecz.id_meczu'), nullable=False)

class Mecz(db.Model):
    id_meczu = db.Column(db.Integer, primary_key=True)
    data_meczu = db.Column(db.Date, default=func.today(), nullable=False)
    liga = db.Column(db.String(100), nullable=False)
    dr1 = db.Column(db.String(80), nullable=False)
    dr2 = db.Column(db.String(80), nullable=False)
    wynik_meczu = db.Column(db.String(1))
    dokladny_wynik = db.Column(db.String(10))
    kurs = db.relationship('Kursy')
    zaklad = db.relationship('Zaklad')

class Zaklad(db.Model):
    id_zakladu = db.Column(db.Integer, primary_key=True)
    kurs = db.Column(db.Float, nullable=False)
    typ = db.Column(db.String(1), nullable=False)
    Kupon_id_kuponu = db.Column(db.Integer, db.ForeignKey('kupon.id_kuponu'))
    Mecz_id_meczu = db.Column(db.Integer, db.ForeignKey('mecz.id_meczu'))
    stan= db.Column(db.String(20))

class Kupon(db.Model):
    id_kuponu = db.Column(db.Integer, primary_key=True)
    data_zakonczenia = db.Column(db.Date, default=func.today())
    kwota = db.Column(db.Integer)
    kurs = db.Column(db.Float)
    potencjalna_wygrana = db.Column(db.Float)
    stan = db.Column(db.String(20))
    Klient_id_user = db.Column(db.Integer, db.ForeignKey('uzytkownik.id_user'))

class Portfel(db.Model):
    id_portfela = db.Column(db.Integer, primary_key=True)
    id_klienta = db.Column(db.Integer, nullable=False)
    stan = db.Column(db.Float, nullable=False)
    Klient_id_user = db.Column(db.Integer, db.ForeignKey('uzytkownik.id_user'))
    wplata = db.relationship('Wplata',cascade="all, delete-orphan")
    wyplata = db.relationship('Wyplata',cascade="all, delete-orphan")

class Wplata(db.Model):
    id_wplaty = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, default=datetime.today(), nullable=False)
    kwota = db.Column(db.Float, nullable=False)
    czy_z_kuponu = db.Column(db.String(1), nullable=False)
    Portfel_id_portfela = db.Column(db.Integer, db.ForeignKey('portfel.id_portfela', ondelete='CASCADE'))


class Wyplata(db.Model):
    id_wypłaty = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, default=datetime.today(), nullable=False)
    kwota = db.Column(db.Float, nullable=False)
    czy_z_kuponu = db.Column(db.String(1), nullable=False)
    Portfel_id_portfela = db.Column(db.Integer, db.ForeignKey('portfel.id_portfela', ondelete='CASCADE'))

    
@event.listens_for(Portfel, "before_delete")
def receive_before_delete(mapper, connection, target):
    for child in target.children:
        connection.delete(child)