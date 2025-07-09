
from flask import Flask, render_template, redirect, url_for, request
from models import db, User, Task
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)

# Create Tables
with app.app_context():
    db.create_all()

# Flask login
login_manager = LoginManager()
# redirects here if @login_required fails
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required



def home():
    return "Hello world"

if __name__ == '__main__':
    app.run(debug=True)

