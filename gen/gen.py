from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from models import db, Book, Review, User, Like
from sqlalchemy import and_
import datetime

gen_bp = Blueprint('gen', __name__, url_prefix='/', template_folder="templates")

@gen_bp.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    global books
    books = Book.query.order_by(Book.title)
    if request.method == "POST":
        results = Book.query.filter(Book.title.like(request.form["search"] + '%')).all() 
        results = results + Book.query.filter(Book.title.like('% ' + request.form["search"] + '%')).all()
        results = list(dict.fromkeys(results))
        return render_template("/gen/search.html", results=results, books=books)
    return render_template("/gen/search.html", books=books)

@gen_bp.route('/book', methods=['GET', 'POST'])
@login_required
def book():
    global book
    global reviews
    global likes
    global users
    if request.method == "POST":
        book = Book.query.filter(Book.title == request.form["bookName"]).first() 
        users = User.query.all()
        reviews = Review.query.all()
        users = User.query.all()
        likes = Like.query.all()
        return render_template("/gen/book.html", users=users, reviews=reviews, book=book, likes=likes)
    return render_template("/gen/search.html", books=books)

@gen_bp.route('/review', methods=['GET', 'POST'])
@login_required
def review():
    if request.method == "POST":
        text = request.form["review"]
        title = request.form["title"]
        rating = request.form["rating"]
        x = datetime.datetime.now()
        newReview = Review(bookID = book.id, userID = current_user.id, publishing_date = x.strftime("%x"), title = title, text = text, rating = rating)
        db.session.add(newReview)
        db.session.commit()
        reviews = Review.query.all()
        users = User.query.all()
        return render_template("/gen/book.html", users=users, reviews=reviews, book=book, likes=likes)
    return render_template("/gen/book.html", users=users, reviews=reviews, book=book, likes=likes)

@gen_bp.route('/like', methods=['GET', 'POST'])
@login_required
def like():
    if request.method == "POST":
        if Like.query.filter(and_(Like.userID == current_user.id, Like.reviewID == request.form.get("reviewID"), Like.like == 1, Like.dislike == 0)).first() == None:
            newLike = Like(reviewID = request.form.get("reviewID"), userID = current_user.id, like = 1, dislike = 0)
            db.session.add(newLike)
            db.session.commit()
            if Like.query.filter(and_(Like.userID == current_user.id, Like.reviewID == request.form["reviewID"], Like.like == 0, Like.dislike == 1)).first() != None:
                Like.query.filter(and_(Like.userID == current_user.id, Like.reviewID == request.form["reviewID"], Like.like == 0, Like.dislike == 1)).delete()
                db.session.commit()
            likes = Like.query.all()
            likeCount = 0
            dislikeCount = 0
            for like in likes:
                if int(request.form["reviewID"]) == like.reviewID:
                    likeCount = likeCount + int(like.like)
                    dislikeCount = dislikeCount + int(like.dislike)
            review = request.form.get("reviewID")
            return render_template("/gen/button.html", likeCount=likeCount, dislikeCount=dislikeCount, review=review)
        else:
            Like.query.filter(and_(Like.userID == current_user.id, Like.reviewID == request.form.get("reviewID"), Like.like == 1, Like.dislike == 0)).delete()
            db.session.commit()
            likes = Like.query.all()
            likeCount = 0
            dislikeCount = 0
            for like in likes:
                if int(request.form["reviewID"]) == like.reviewID:
                    likeCount = likeCount + int(like.like)
                    dislikeCount = dislikeCount + int(like.dislike)
            review = request.form.get("reviewID")
            return render_template("/gen/button.html", likeCount=likeCount, dislikeCount=dislikeCount, review=review)
    return render_template("/gen/book.html", users=users, reviews=reviews, book=book, likes=likes)

@gen_bp.route('/dislike', methods=['GET', 'POST'])
@login_required
def dislike():
    if request.method == "POST":
        if Like.query.filter(and_(Like.userID == current_user.id, Like.reviewID ==  request.form.get("reviewID"), Like.like == 0, Like.dislike == 1)).first() == None:
            newDislike= Like(reviewID = request.form.get("reviewID"), userID = current_user.id, like = 0, dislike = 1)
            db.session.add(newDislike)
            db.session.commit()
            if Like.query.filter(and_(Like.userID == current_user.id, Like.reviewID == request.form["reviewID"], Like.like == 1, Like.dislike == 0)).first() != None:
                Like.query.filter(and_(Like.userID == current_user.id, Like.reviewID == request.form["reviewID"], Like.like == 1, Like.dislike == 0)).delete()
                db.session.commit()
            likes = Like.query.all()
            likeCount = 0
            dislikeCount = 0
            for like in likes:
                if int(request.form["reviewID"]) == like.reviewID:
                    likeCount = likeCount + int(like.like)
                    dislikeCount = dislikeCount + int(like.dislike)
            review = request.form.get("reviewID")
            return render_template("/gen/button.html", likeCount=likeCount, dislikeCount=dislikeCount, review=review)
        else:
            Like.query.filter(and_(Like.userID == current_user.id, Like.reviewID == request.form.get("reviewID"), Like.like == 0, Like.dislike == 1)).delete()
            db.session.commit()
            likes = Like.query.all()
            likeCount = 0
            dislikeCount = 0
            for like in likes:
                if int(request.form["reviewID"]) == like.reviewID:
                    likeCount = likeCount + int(like.like)
                    dislikeCount = dislikeCount + int(like.dislike)
            review = request.form.get("reviewID")
            return render_template("/gen/button.html", likeCount=likeCount, dislikeCount=dislikeCount, review=review)
    return render_template("/gen/book.html", users=users, reviews=reviews, book=book, likes=likes)

@gen_bp.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if int(current_user.role) == 1:
        if request.method == "POST":
            newBook = Book(title = request.form["title"], author = request.form["author"], genre = request.form["genre"], publishing_date = request.form["publishing_date"], blurb = request.form["blurb"], cover_link = request.form["cover_link"])
            db.session.add(newBook)
            db.session.commit()
            return redirect(url_for('gen.search'))
        return render_template("/gen/admin.html")
    else:
        return redirect(url_for('gen.search'))