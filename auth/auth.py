from flask import Blueprint, render_template, redirect, url_for, request, flash, Flask
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models import db, User
import os

folderPath = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
UPLOAD_FOLDER = folderPath.replace('\\auth', '') + '\\static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

auth_bp = Blueprint('auth', __name__, url_prefix='/', template_folder="templates")

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        user = User.query.filter(User.username == request.form["username"]).first()
        if user:
            if check_password_hash(user.password, request.form["password"]):
                #success
                login_user(user)
                return redirect(url_for('gen.search'))
            else:
                flash("Invalid password", "error")
        else:
            flash("Invalid username", "error")
    return render_template("/auth/login.html")

@auth_bp.route('/signup', methods=['GET', "POST"])
def signup():
    if request.method == "POST":
        u = User.query.filter(User.username == request.form["username"]).first()
        e = User.query.filter(User.email == request.form["email"]).first()
        if u == None:
            if e == None:
                image = request.files['imagePicker']
                if image and allowed_file(image.filename):
                    filename = secure_filename(image.filename)
                    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                    hashedPass = generate_password_hash(request.form["password"])
                    newUser = User(username = request.form["username"], password = hashedPass, email = request.form["email"], bio = request.form["bio"], profile_picture = image.filename)
                    db.session.add(newUser)
                    db.session.commit()
                    return redirect(url_for('auth.login'))
                else:
                    flash('File not an image')
                    return render_template("/auth/signup.html")
            else:
                flash('No duplicate emails allowed')
                return render_template("/auth/signup.html")
        else:
            flash('No duplicate usernames allowed')
            return render_template("/auth/signup.html")
    return render_template("/auth/signup.html")

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))