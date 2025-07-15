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


## 📁 File Structure

mini-task-manager/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── forms.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth_routes.py
│   │   └── task_routes.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   └── edit_task.html
│   ├── static/  # (Optional: CSS/JS files)
│   └── extensions.py
│
├── migrations/
│
├── instance/
│   └── database.db
│
├── config.py
├── run.py
└── requirements.txt

