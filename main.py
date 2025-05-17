import os
from math import trunc

from flask import Flask, render_template, redirect, url_for, jsonify, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
import logging
from asgiref.wsgi import WsgiToAsgi
from sqlalchemy import false

logging.basicConfig(level=logging.DEBUG)
uvicorn_ws_enabled = os.getenv('UVICORN_WS', 'on') == 'on'

app = Flask(__name__)

secret_key = 'cdd303f0-d70a-4e36-a9f7-f94a14b59942'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://<user>:<password>@<host>:<port>/<database>'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secret_key

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    admin = db.Column(db.Boolean, nullable=False)



@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == "POST":
        role = request.form.get('role')
        userid = request.form.get('userid')
        password = request.form.get('password')
        user = User.query.filter_by(userid=userid).first()
        if user:
            # logging.debug(f"Retrieved password hash from database: {user.password}")
            if bcrypt.check_password_hash(user.password, password):
                flash('You were successfully logged in!')
                login_user(user)
                if role == 'admin' and current_user.admin:
                    return redirect(url_for('dashboard_admin'))
                elif role == 'student' and not current_user.admin:
                    return redirect(url_for('dashboard_student'))
                else:
                    flash("Something went wrong try again!")
            else:
                flash("Password is incorrect!!!", "error")
        else:
            flash("User does not exists!!!", "error")
    return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You were logged out!')
    return redirect(url_for('login'))

@app.route('/checkin')
@login_required
def checkin():
    return render_template("checkin.html")

@app.route('/checkout')
@login_required
def checkout():
    return render_template("checkout.html")

@app.route('/dashboard-student')
@login_required
def dashboard_student():
    if not current_user.admin: return render_template("dashboard_student.html")
    else: return redirect(url_for('dashboard_admin'))

@app.route('/dashboard-admin')
@login_required
def dashboard_admin():
    if current_user.admin: return render_template("dashboard_admin.html")
    else: return redirect(url_for('dashboard_student'))

@app.route('/room-status', methods=['GET'])
@login_required
def room_status():
    floor_data = {
        2: ["201", "202", "203", "204", "205", "206", "207", "208", "209", "210"],
        3: ["301", "302", "303", "304", "305", "306", "307", "308", "309", "310", "311", "312", "313", "314", "315"],
        4: ["401", "402", "403", "404", "405", "406", "407", "408", "409", "410", "411", "412", "413", "414", "415"],
        5: ["501", "502", "503", "504", "505", "506", "507", "508", "509", "510", "511", "512", "513", "514", "515"],
        6: ["601", "602", "603", "604", "605", "606", "607", "608", "609", "610", "611", "612", "613", "614", "615"],
        7: ["701", "702", "703", "704", "705", "706", "707", "708", "709", "710", "711", "712", "713", "714", "715"]
    }

    occupied_rooms = ["202", "203", "305", "404", "505", "603"]

    floor = request.args.get('floor', type=int)
    rooms = floor_data.get(floor) if floor else None

    return render_template(
        'roomstatus.html',
        selected_floor=floor,
        rooms=rooms,
        occupied_rooms=occupied_rooms
    )

@app.route('/students-list')
def students_list():
    return render_template("studentsList.html")



def admin_db():
    with app.app_context():
        hashed_password = bcrypt.generate_password_hash("password123#").decode("utf-8")
        user = User.query.filter_by(userid="2200000").first()
        if not user:
            new_user = User(userid="2200000", password=hashed_password, admin=True)
            db.session.add(new_user)
            db.session.commit()
            print("Admin user created.")
        else:
            print("Admin user already exists.")



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    admin_db()
    app.run(host="0.0.0.0")
