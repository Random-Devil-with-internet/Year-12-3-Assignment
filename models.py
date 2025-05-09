from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.sql.operators import ilike_op,like_op

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(128), nullable=False)
    bio = db.Column(db.Text)
    profile_picture = db.Column(db.String(200))
    
    def __repr__(self):
        return f"<User {self.id} - {self.username}>"