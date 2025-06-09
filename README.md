# 🏠 KBU Dormitory Check-in/Check-out System

기숙사에 입실/퇴실하는 학생과 관리자를 위한 웹 기반 시스템입니다.  
학생은 자신의 상태와 방 정보를 확인하고, 퇴실 신청을 할 수 있으며,  
관리자는 전체 학생의 입퇴실 상태를 관리할 수 있습니다.

---

## 📌 주요 기능

### 👨‍🎓 학생
- 로그인 후 대시보드에서 본인 정보 확인
- 입실 상태 확인 및 퇴실 신청
- 프로필 접근

### 🛠️ 관리자
- 전체 학생 목록 확인
- 학생 입실 / 퇴실 처리
- 방 상태 관리

---

## 🖼️ 화면 구성
- `/login` – 역할(학생/관리자) 선택 로그인 화면
- `/dashboard_student` – 학생 대시보드
- `/dashboard_admin` – 관리자 대시보드
- `/checkin`, `/checkout` – 입퇴실 처리 페이지
- `/roomstatus`, `/studentsList` – 방 상태 및 전체 학생 목록
- `/my_request`, `/requests` – 신청 내역

---

## 🛠️ 기술 스택
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python Flask
- **Template Engine**: Jinja2
- **Others**: Jinja `url_for`, form POST 처리 등

---

## 🧱 폴더 구조
```
dorm-project/
├── static/
│   └── style.css              # 전체 스타일 정의
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
├── main.py                     # Flask 애플리케이션 엔트리포인트
├── pyvenv.cfg                  # 가상환경 설정
├── requirements.txt            # 설치 패키지 목록
└── README.md
```

---

## 🚀 실행 방법
1. 가상환경 실행 (선택)
```bash
python -m venv venv
source venv/bin/activate  # 또는 venv\Scripts\activate (Windows)
```

2. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

3. Flask 앱 실행
```bash
python main.py
```

4. 브라우저에서 확인
```
http://localhost:5000
또는 배포 도메인: http://dorm-kbu.kr
```

---

## 🙋‍♂️ 제작자
- 프론트엔드: DevFayzullo
- 백엔드: MuzaffarSharofitdinov
