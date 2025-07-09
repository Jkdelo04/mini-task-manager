
from flask import Flask, render_template, redirect, url_for, request
from models import db, User, Task
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)

@app.route('/')



def home():
    return "Hello world"

if __name__ == '__main__':
    app.run(debug=True)

