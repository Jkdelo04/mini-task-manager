# 📝 Mini Task Manager

A full-stack Flask web application that allows users to manage their personal to-do list. Users can register, log in, and create tasks with due dates, completion status, and filters.

## 🚀 Features

- ✅ User Registration & Login (secure with password hashing)
- 📋 Add, Edit, Delete tasks
- 🗓️ Set due dates for tasks
- ✔️ Mark tasks as complete/incomplete
- 🔍 Filter tasks by:
  - Completion status
  - Search term
  - Due date (sort ascending/descending)
- 🧑‍💻 User-specific task dashboard

## Requirements

- Python 3.7+
- Virtual environment (recommended)
- Flask and dependencies (see `requirements.txt`)

---

## ⚙️ Setup and Usage Guide

### 2. Create and activate a virtual environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment (optional)

By default, the app uses `DevelopmentConfig` from `config.py`.  
No extra setup is needed unless customization is required.

### 5. Initialize the database

```bash
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

### 6. Run the application

**Using Flask CLI:**
```bash
flask run
```

**Or directly with Python:**
```bash
python run.py
```

The app will be available at [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📁 Project Structure

```
mini-task-manager/
│
├── app/
│   ├── __init__.py        # App factory and extensions
│   ├── models.py          # SQLAlchemy models
│   ├── forms.py           # WTForms
│   ├── routes/
│   │   ├── __init__.py    # Blueprint registration
│   │   ├── auth_routes.py # Authentication routes
│   │   └── task_routes.py # Task CRUD routes
│   └── templates/         # Jinja2 HTML templates
│
├── migrations/            # Database migration files
├── config.py              # Configuration file
├── requirements.txt       # Dependencies list
├── run.py                 # Application entry point
└── README.md              # Project documentation
```

---

## 🧩 Notes

- `database.db` will be stored inside the `instance/` folder.
- Passwords are securely hashed using bcrypt.
- Protected routes require login via Flask-Login.
- Blueprints help organize and modularize your routes.

---

## 🆘 Troubleshooting

- 🔧 Missing templates or broken routes? Check blueprint registrations.
- 🧮 Changed models? Run a migration and upgrade the database:
  ```bash
  flask db migrate -m "Your message"
  flask db upgrade
  ```
- 🖥️ Review console output for any error details.

---

## 📄 License

This project is open source and available under the [MIT License](https://opensource.org/licenses/MIT).
  
