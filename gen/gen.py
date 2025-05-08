from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, login_required, logout_user
from models import db, User

gen_bp = Blueprint('gen', __name__, url_prefix='/', template_folder="templates")

@gen_bp.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == "POST":
        result = User.query.filter(User.username == request.form["search"]).first()
        return render_template("/gen/home.html", result=result)
    return render_template("/gen/home.html")