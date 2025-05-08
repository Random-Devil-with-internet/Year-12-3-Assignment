from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, login_required, logout_user
from models import db, User

gen_bp = Blueprint('gen', __name__, url_prefix='/', template_folder="templates")

@gen_bp.route('/home', methods=['GET', 'POST'])
@login_required
def Home():
    return render_template("/gen/home.html")