from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Kursy
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        flash('Welcme to SQLBET!', category='success')

    return render_template("home.html", user=current_user)


