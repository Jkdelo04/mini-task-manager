import os
from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from datetime import datetime
from sqlalchemy import asc
from datetime import date


app = Flask(__name__, instance_relative_config=True)
app.config['SECRET_KEY'] = 'thisisasecretkey'

db_path = os.path.join(app.instance_path, 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))  # changed from title
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    due_date = db.Column(db.Date, nullable=True)



class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(),Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(),Length(min=4, max=20)], render_kw={"placeholder": "password"})
    submit = SubmitField("Register")
    
    def validate_username (self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError("Username is already taken. Please choose a different one!")
        
class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(),Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(),Length(min=4, max=20)], render_kw={"placeholder": "password"})
    submit = SubmitField("Login")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    # Show Tasks
    task_list = Task.query.filter_by(user_id=current_user.id).order_by(asc(Task.due_date)).all()
    today = date.today()

    return render_template('dashboard.html', task_list=task_list, today=today)

@app.route('/add', methods=['POST'])
def add():
    name = request.form.get("name")  
    due_date_str = request.form.get("due_date")

    due_date = None
    if due_date_str:
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        except ValueError:
            pass  # Handle bad date input silently or with feedback

    new_task = Task(name=name, complete=False, user_id=current_user.id, due_date=due_date)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/Update/<int:task_id>')
def update(task_id):
    task = Task.query.filter_by(id=task_id).first()
    task.complete = not task.complete
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/Delete/<int:task_id>')
def delete(task_id):
    task = Task.query.filter_by(id=task_id).first()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('dashboard'))

@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    # DEBUG: print any validation errors
    if form.errors:
        print("Form errors:", form.errors)

    return render_template('register.html', form=form)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
    
    app.run(debug=True)
