from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), unique=True, nullable=False)
    author = db.Column(db.String(20), nullable=False)
    genre = db.Column(db.String(20), nullable=False)
    publishing_date = db.Column(db.String(20))
    blurb = db.Column(db.Text)
    cover_link = db.Column(db.String(200))
    
    def __repr__(self):
        return f"<User {self.id} - {self.title}>"
    
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(128), nullable=False)
    bio = db.Column(db.Text)
    profile_picture = db.Column(db.String(200), nullable=False)
    
    def __repr__(self):
        return f"<User {self.id} - {self.username}>"    
    
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bookID = db.Column(db.Integer, db.ForeignKey(Book.id), nullable=False)
    userID = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    publishing_date = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f"<User {self.id} - {self.title}>"