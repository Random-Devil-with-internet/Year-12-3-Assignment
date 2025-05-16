from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, login_required, logout_user
from models import db, Book, Review, User
from sqlalchemy.sql.operators import ilike_op
import datetime

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
def book():
    if request.method == "POST":
        global book
        book = Book.query.filter(Book.title == result).first() 
        global reviews
        reviews = Review.query.all()
        global users
        users = User.query.all()
        return render_template("/gen/book.html", users=users, reviews=reviews, book=book)
    return render_template("/gen/search.html")

@gen_bp.route('/review', methods=['GET', 'POST'])
@login_required
def review():
    if request.method == "POST":
        text = request.form["review"]
        title = request.form["title"]
        x = datetime.datetime.now()
        newReview = Review(bookID = book.id, userID = current_user.id, publishing_date = x.strftime("%x"), title=title, text = text)
        db.session.add(newReview)
        db.session.commit()
        reviews = Review.query.all()
        users = User.query.all()
        return render_template("/gen/book.html", users=users, reviews=reviews, book=book)
    return render_template("/gen/book.html")