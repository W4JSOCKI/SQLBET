from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Kursy
from . import db
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