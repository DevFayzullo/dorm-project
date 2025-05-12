from flask import render_template, Flask, request

app =  Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/checkin')
def checkin():
    return render_template("checkin.html")

@app.route('/checkin-admin')
def checkin_admin():
    return render_template("checkinAdmin.html")

@app.route('/checkout')
def checkout():
    return render_template("checkout.html")

@app.route('/checkout-admin')
def checkout_admin():
    return render_template("checkoutAdmin.html")

@app.route('/dashboard-student')
def dashboard_student():
    return render_template("dashboard_student.html")

@app.route('/dashboard-admin')
def dashboard_admin():
    return render_template("dashboard_admin.html")

@app.route('/room-status', methods=['GET'])
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

# @app.route('/<name>')
# def hello(name=None):
#     return render_template('hello.html', person=name)
if __name__ == "__main__":
    app.run(debug=True)