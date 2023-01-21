from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
import json

portfel = Blueprint('portfel', __name__)


@portfel.route('/portfel', methods=['GET', 'POST'])
@login_required
def home():
   
        

    return render_template("portfel.html", user=current_user)

