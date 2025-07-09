# Create Users and Tasks
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# User
class User(db.Model, UserMixin):
    # Unique ID for each user
    id = db.Column(db.Integer, primary_key = True)

    # Username (Make sure it is Unique and not empty)
    username = db.Column(db.String(150), nullable = False, unique = True)
    # Hashed PW
    password = db.Column(db.String(150), nullable = False)


# Task
class Task(db.Model):
    # Unique ID for each task
    id = db.Column(db.Integer, primary_key = True)

    # Title of task
    title = db.Column(db.String(255))
    # Status of the task
    complete = db.Column(db.Boolean, default = False)
    # Link the user to the task
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))