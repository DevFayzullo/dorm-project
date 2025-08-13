# 🏠 KBU Dormitory Check-in/Check-out System

[🇰🇷 한국어 README](./README.kr.md)

A web-based management system designed for students and administrators of the KBU dormitory.  
Students can check their room and status, request check-out, and view their profile.  
Administrators can manage the overall check-in/check-out status and room information.

---

## 📌 Main Features

### 👨‍🎓 Students
- Login and view personal dashboard
- Check current dormitory status
- Submit check-out request
- Access personal profile

### 🛠️ Administrators
- View full student list
- Approve or process student check-in/check-out
- Manage room status

---

## 🖼️ Pages Overview
- `/login` – Role selection (Student/Admin) login
- `/dashboard_student` – Student dashboard
- `/dashboard_admin` – Admin dashboard
- `/checkin`, `/checkout` – Check-in / Check-out process pages
- `/roomstatus`, `/studentsList` – Room status and full student list
- `/my_request`, `/requests` – Request history

---

## 🛠️ Tech Stack
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python Flask
- **Template Engine**: Jinja2
- **Others**: Flask `url_for`, POST form handling

---

## 📂 Project Structure
```
dorm-project/
├── static/
│   └── style.css              # Global styles
├── templates/
│   ├── login.html
│   ├── dashboard_student.html
│   ├── dashboard_admin.html
│   ├── checkin.html
│   ├── checkout.html
│   ├── roomstatus.html
│   ├── studentsList.html
│   ├── 404.html
│   ├── my_request.html
│   └── requests.html
├── main.py                     # Flask app entry point
├── pyvenv.cfg                   # Virtual environment settings
├── requirements.txt             # Python dependencies
└── README.md
```

---

## 🚀 How to Run
1. **(Optional)** Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the Flask application**:
```bash
python main.py
```

4. **Access in browser**:
```
http://localhost:5000
or deployed domain: http://dorm-kbu.kr
```

---

## 🙋‍♂️ Authors
- **Frontend**: DevFayzullo
- **Backend**: MuzaffarSharofitdinov

---

## 📄 License
This project is created for educational purposes as part of the **University Capstone Design Project**.
