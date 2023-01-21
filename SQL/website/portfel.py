from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
import json

portfel = Blueprint('portfel', __name__)


@portfel.route('/portfel', methods=['GET', 'POST'])
@login_required
def home():
    #TODO - add button to add new wallet
    #TODO - take wallets from database
    #TODO - redirect to wallets after clicking on buttons
    button_tags =["Portfel #1","Portfel #2","Portfel #3"]

    return render_template("portfel.html", user=current_user,button_tags=button_tags)

