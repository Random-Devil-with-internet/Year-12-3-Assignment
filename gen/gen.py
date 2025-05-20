from flask import Blueprint, render_template, request
from flask_login import current_user, login_required
from models import db, Book, Review, User
import datetime

gen_bp = Blueprint('gen', __name__, url_prefix='/', template_folder="templates")

@gen_bp.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == "POST":
        results = Book.query.filter(Book.title.like(request.form["search"] + '%')).all()
        return render_template("/gen/search.html", results=results)
    return render_template("/gen/search.html")

@gen_bp.route('/book', methods=['GET', 'POST'])
@login_required
def book():
    if request.method == "POST":
        global book
        book = Book.query.filter(Book.title == request.form["review"]).first() 
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