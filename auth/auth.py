from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth', template_folder="templates")

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        user = User.query.filter(User.username == request.form["username"]).first()
        if user:
            if check_password_hash(user.password, request.form["password"]):
                #success
                login_user(user)
                return redirect(url_for('gen.index')) #my other blueprint is gen (for general)
            else:
                flash("Invalid password", "error")
        else:
            flash("Invalid username", "error")
    return render_template("auth/login.html")

@auth_bp.route('/signup', methods=['GET', "POST"])
def signup():
    if request.method == "POST":
        hashedPass = generate_password_hash(request.form["password"])
        newUser = User(username = request.form["username"], password = hashedPass)
        db.session.add(newUser)
        db.session.commit()
        return redirect(url_for('auth.login'))
    
    return render_template('auth/signup.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login')) # you need to make sure that when using url_for(