from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, login_required, logout_user
from models import db, Book
from sqlalchemy.sql.operators import ilike_op

gen_bp = Blueprint('gen', __name__, url_prefix='/', template_folder="templates")

@gen_bp.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == "POST":
        global result
        result = db.session.scalar(db.select(Book.title).filter(ilike_op(Book.title, request.form["search"] + '%')))
        return render_template("/gen/search.html", result=result)
    return render_template("/gen/search.html")

@gen_bp.route('/movie', methods=['GET', 'POST'])
@login_required
def movie():
    if request.method == "POST":
        book = Book.query.filter(Book.title == result).first() 
        return render_template("/gen/movie.html", book=book)
    return render_template("/gen/search.html")