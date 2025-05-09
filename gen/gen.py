from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, login_required, logout_user
from models import db, User
from sqlalchemy.sql.operators import ilike_op

gen_bp = Blueprint('gen', __name__, url_prefix='/', template_folder="templates")

@gen_bp.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == "POST":
        result = db.session.scalar(db.select(User.username).filter(ilike_op(User.username, request.form["search"] + '%')))
        return render_template("/gen/home.html", result=result)
    return render_template("/gen/home.html")