# AvatarApp - Django Advanced Project

A personality quiz web application built with Django.

## 🚀 Main Features

* User registration, login, profile editing, and password change
* Paginated personality quiz with Big Five scoring
* Results saved to profile and displayed on user dashboard
* Feedback and contact forms with validation
* Admin panel with full and limited access roles (SuperAdmin / Staff)

## 🔐 Admin Setup

* Admin interface with custom search, filters, and list displays
* Two admin groups: SuperAdmin (full CRUD), Staff (limited access)

## 🧪 Testing Setup

To load initial quiz data (traits, questions, and answers):

```bash
python3 manage.py loaddata fixtures/initial_data.json
```

## ⚙️ Run Locally

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

Project by **Kalin Kolev** for the Django Advanced Course Final Exam
