import datetime
import logging
import os

today = datetime.date.today().isoformat()

from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

from asgiref.wsgi import WsgiToAsgi

logging.basicConfig(level=logging.DEBUG)
uvicorn_ws_enabled = os.getenv('UVICORN_WS', 'on') == 'on'

app = Flask(__name__)

secret_key = 'cdd303f0-d70a-4e36-a9f7-f94a14b59942'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://avnadmin:AVNS_QHbuDuXH6nTNUi9IvFo@postgres-smartboy.h.aivencloud.com:26207/dorm?sslmode=require'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://<username>:<password>@<host>:<port>/<database>'
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
    full_name = db.Column(db.String(150), nullable=False)
    room = db.Column(db.Integer, nullable=True)
    phone_number = db.Column(db.String(30), nullable=False)
    admin = db.Column(db.Boolean, nullable=False)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(10), nullable=False)
    floor = db.Column(db.Integer, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    current_occupants = db.Column(db.Integer, default=0)

class Requests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.String(15), unique=True, nullable=False)
    student_name = db.Column(db.String(100), nullable=False)
    student_id = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    room_number = db.Column(db.String(10), nullable=False)
    checkout_date = db.Column(db.String(10), nullable=False)
    request_type = db.Column(db.String(10), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class MyRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), nullable=False)
    request_id = db.Column(db.String(15), unique=True, nullable=False)
    status = db.Column(db.String(10), nullable=False)
    request_type = db.Column(db.String(10), nullable=False)

def already(user_id):
    return (Requests.query.filter_by(student_id=user_id).first() is not None or MyRequest.query.filter_by(student_id=user_id).first() is not None)

@app.route('/')
@login_required
def index():
    if current_user.is_authenticated and current_user.admin:text = "📊 관리자 대시보드"
    elif current_user.is_authenticated and not current_user.admin:text = "👨‍🎓 학생 대시보드"
    else:text = "🔐 로그인"
    return render_template("index.html", text=text)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and current_user.admin:
        return redirect(url_for('dashboard_admin'))
    elif current_user.is_authenticated and not current_user.admin:
        return redirect(url_for('dashboard_student'))

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

@app.route('/checkin', methods=['GET', 'POST'])
@login_required
def checkin():
    floors = db.session.query(Room.floor).distinct().all()
    floors = sorted([f[0] for f in floors])

    if already(current_user.userid):
        return redirect(url_for("index"))

    if current_user.room:
        return redirect(url_for("index"))

    if request.method == 'GET':
        return render_template('checkin.html', step=1, floors=floors)

    step = int(request.form.get('step', 1))
    direction = request.form.get('direction', 'next')

    if step == 1 and direction == "next":
        return render_template('checkin.html', step=2,floors=floors,date=today)
    elif step == 2 and direction == "back":
        return render_template('checkin.html', step=1,floors=floors,date=today)
    elif step == 2 and direction == "next":
        room = request.form['room']
        return render_template('checkin.html', step=3,floors=floors,room=room,date=today)
    elif step == 3 and direction == "back":
        room = request.form['room']
        return render_template('checkin.html', step=2,floors=floors,room=room,date=today)
    elif step == 3:
        studentName = request.form['name']
        studentId = request.form['studentId']
        phone = request.form['phone']
        date = request.form['date']
        room = request.form['room']
        request_type = request.form['checkin']

        last_request = db.session.query(func.max(Requests.request_id)).scalar()

        if last_request:
            new_id = int(last_request[4:]) + 1
        else:
            new_id = 1

        formatted_request_id = f"REQ-{new_id:05d}"

        request_obj = Requests(
            request_id=formatted_request_id,
            student_name=studentName,
            student_id=studentId,
            phone=phone,
            room_number=room,
            checkout_date=date,
            request_type=request_type,
            reason=""
        )

        my_request = MyRequest(
            student_id=studentId,
            request_id=formatted_request_id,
            status="Pending...",
            request_type=request_type
        )

        db.session.add(request_obj)
        db.session.add(my_request)
        db.session.commit()

        flash(f'Request submitted successfully! Your Request ID: {formatted_request_id}', 'success')
        return redirect(url_for('my_request'))

    return None


@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():

    if already(current_user.userid):
        return redirect(url_for("index"))

    if not current_user.room:
        return redirect(url_for("index"))

    if request.method == "GET":
        return render_template('checkout.html', step=1)

    step = int(request.form.get('step', 1))
    direction = request.form.get('direction', 'next')

    if step == 1 and direction == "next":
        return render_template('checkout.html', step=2,date=today)
    elif step == 2 and direction == "back":
        return render_template('checkout.html', step=1,date=today)
    elif step == 2 and direction == "next":
        return render_template('checkout.html', step=3,date=today)
    elif step == 3 and direction == "back":
        return render_template('checkout.html', step=2,date=today)
    elif step == 3:
        studentName = request.form['studentName']
        studentId = request.form['studentId']
        phone = request.form['phone']
        room = request.form['room']
        date = request.form['date']
        reason = request.form['reason']
        request_type = request.form['checkout']

        last_request = db.session.query(func.max(Requests.request_id)).scalar()

        if last_request:
            new_id = int(last_request) + 1
        else:
            new_id = 1

        formatted_request_id = f"REQ-{new_id:05d}"

        request_obj = Requests(
            request_id=formatted_request_id,
            student_name=studentName,
            student_id=studentId,
            phone=phone,
            room_number=room,
            checkout_date=date,
            request_type=request_type,
            reason=reason
        )

        my_request = MyRequest(
            student_id=studentId,
            request_id=formatted_request_id,
            status="Pending...",
            request_type=request_type
        )

        db.session.add(request_obj)
        db.session.add(my_request)
        db.session.commit()

        flash(f'Request submitted successfully! Your Request ID: {formatted_request_id}', 'success')
        return redirect(url_for('my_request'))
    return None

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

@app.route('/room-status/<int:floor>')
@login_required
def available_rooms(floor):
    rooms = Room.query.filter_by(floor=floor).filter(Room.current_occupants < Room.capacity).all()
    room_numbers = [room.room_number for room in rooms]
    return jsonify({'rooms': room_numbers})

@app.route('/room-status', methods=['GET'])
@login_required
def room_status():
    # Qavat raqamini olish (masalan: 2–7)
    floor = request.args.get('floor', type=int)
    rooms = None
    occupied_rooms = []
    if floor:
        room_objs = Room.query.filter_by(floor=floor).order_by(Room.room_number).all()
        rooms = [room.room_number for room in room_objs]
        occupied_rooms = [room.room_number for room in room_objs if room.current_occupants >= room.capacity]
    return render_template(
        'roomstatus.html',
        selected_floor=floor,
        rooms=rooms,
        occupied_rooms=occupied_rooms
    )

@app.route('/students-list', methods=['GET'])
@login_required
def students_list():
    userid = request.args.get('userid')  # qidiruv inputidan
    user = None
    if userid:
        user = User.query.filter_by(userid=userid).first()
    return render_template("studentsList.html", user=user)




@app.route('/requests')
@login_required
def requests():
    _requests = Requests.query.order_by(Requests.submitted_at.desc()).all()
    return render_template('requests.html', requests=_requests)

@app.route('/my-request', methods=['GET', 'POST'])
@login_required
def my_request():
    _myrequest = ""
    _request = ""
    try:
        _myrequest = MyRequest.query.filter_by(student_id=current_user.userid).first()
        _request = Requests.query.filter_by(student_id=current_user.userid).order_by(Requests.id.desc()).first()
    except:
        pass

    if request.method == "POST":
        delete = request.form["delete"]
        if delete:
            req = Requests.query.filter_by(student_id=current_user.userid).first()
            my_req = MyRequest.query.filter_by(student_id=current_user.userid).first()
            if req and my_req:
                db.session.delete(req)
                db.session.delete(my_req)
                db.session.commit()
        return redirect(url_for('my_request'))

    return render_template('my_request.html', my_request=_myrequest, request=_request)

def admin_db():
    with app.app_context():
        hashed_password = bcrypt.generate_password_hash("password123#").decode("utf-8")
        user = User.query.filter_by(userid="2200000").first()
        if not user:
            new_user = User(userid="2200000", password=hashed_password, full_name="홍길동", room=330, phone_number="010-1234-5678", admin=True)
            db.session.add(new_user)
            db.session.commit()
            print("Admin user created.")
        else:
            print("Admin user already exists.")

# asgi_app = WsgiToAsgi(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    admin_db()
    app.run(host="0.0.0.0")
