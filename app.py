from flask import Flask, render_template
from flask_login import LoginManager
import os
from models import db, User
from auth.auth import auth_bp
from gen.gen import gen_bp

folderPath = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = '75639702209fe37afc6a854d10d00363'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + folderPath + "/reviews.db"

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(id):
    return db.session.get(User, int(id))

app.register_blueprint(auth_bp)
app.register_blueprint(gen_bp) 

@app.route('/', methods=['GET'])
def index():
    return render_template("/auth/login.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=3000, debug=True)