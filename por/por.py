from flask import Blueprint, render_template, request, Flask, flash
from flask_login import current_user, login_required
from models import db, User, Follow
from werkzeug.utils import secure_filename
import os

folderPath = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
UPLOAD_FOLDER = folderPath.replace('\\por', '') + '\\static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

por_bp = Blueprint('por', __name__, url_prefix='/', template_folder="templates")

@por_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == "POST":
        global name
        global follows
        global users
        follows = Follow.query.all()
        users = User.query.all()
        name = request.form["user"]
        user = User.query.filter(User.username == request.form["user"]).first()
        return render_template("/por/profile.html", user=user, follows=follows, users=users)
    return render_template("/gen/search.html")

@por_bp.route('/change', methods=['GET', 'POST'])
@login_required
def change():
    user = User.query.filter(User.username == request.form["username"]).first()
    if request.method == "POST":
        if user.username == current_user.username:
            return render_template("/por/edit.html", user=user)
        flash('Not your account')
        return render_template("/por/profile.html", user=user, follows=follows, users=users)
    return render_template("/por/profile.html", user=user, follows=follows, users=users)

@por_bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    user = User.query.filter(User.username == name).first()
    if request.method == "POST":
        image = request.files['imagePicker']
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) 
            User.query.filter_by(id=user.id).update({'username':  request.form["username"], 'email': request.form["email"], 'bio': request.form["bio"],  'profile_picture': image.filename})
            db.session.commit()
            user = User.query.filter(User.username == request.form["username"]).first()
            return render_template("/por/profile.html", user=user, follows=follows, users=users)
        return render_template("/por/profile.html", user=user, follows=follows, users=users)
    return render_template("/por/profile.html", user=user, follows=follows, users=users)

@por_bp.route('/follow', methods=['GET', 'POST'])
@login_required
def follow():
    user = User.query.filter(User.username == name).first()
    if request.method == "POST":
        porfileUser = request.form["id"]
        if current_user.id != int(porfileUser):
            check = Follow.query.filter(Follow.user1ID == porfileUser).first()
            if check == None:
                newFollow = Follow(user1ID = porfileUser, user2ID = current_user.id)
                db.session.add(newFollow)
                db.session.commit()
                follows = Follow.query.all()
                users = User.query.all()
                return render_template("/por/profile.html", user=user, follows=follows, users=users)
            users = User.query.all()
            follows = Follow.query.all()
            flash('No duplicate follows')
            return render_template("/por/profile.html", user=user, follows=follows, users=users)
        users = User.query.all()
        follows = Follow.query.all()
        flash('You can not follow your self')
        return render_template("/por/profile.html", user=user, follows=follows, users=users)
    return render_template("/gen/search.html")