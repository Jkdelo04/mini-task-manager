import os
from datetime import datetime, date

from flask import (
    Flask, render_template, url_for, redirect,
    request, flash
)
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    UserMixin, login_user, LoginManager,
    login_required, logout_user, current_user
)
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate


# ------------------ App Configuration ------------------

app = Flask(__name__, instance_relative_config=True)
app.config['SECRET_KEY'] = 'thisisasecretkey'

db_path = os.path.join(app.instance_path, 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)


# ------------------ Login Manager ------------------

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ------------------ Models ------------------

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    due_date = db.Column(db.Date, nullable=True)


# ------------------ Forms ------------------

class RegisterForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Username"}
    )
    password = PasswordField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Password"}
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user = User.query.filter_by(username=username.data).first()
        if existing_user:
            raise ValidationError("Username is already taken. Please choose a different one!")


class LoginForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Username"}
    )
    password = PasswordField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Password"}
    )
    submit = SubmitField("Login")


# ------------------ Routes ------------------

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    if form.errors:
        print("Form errors:", form.errors)

    return render_template('register.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    query = Task.query.filter_by(user_id=current_user.id)

    # Filter and sort options
    search_query = request.args.get('search', '', type=str)
    status_filter = request.args.get('status', 'all', type=str)
    sort_order = request.args.get('sort', 'asc', type=str)
    today = date.today()

    if search_query:
        query = query.filter(Task.name.ilike(f'%{search_query}%'))

    if status_filter == 'complete':
        query = query.filter_by(complete=True)
    elif status_filter == 'incomplete':
        query = query.filter_by(complete=False)

    if sort_order == 'desc':
        query = query.order_by(Task.due_date.desc())
    else:
        query = query.order_by(Task.due_date.asc())

    task_list = query.all()

    return render_template(
        'dashboard.html',
        task_list=task_list,
        today=today,
        search_query=search_query,
        status_filter=status_filter,
        sort_order=sort_order
    )


@app.route('/add', methods=['POST'])
@login_required
def add():
    name = request.form.get("name")
    due_date_str = request.form.get("due_date")

    due_date = None
    if due_date_str:
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        except ValueError:
            pass

    new_task = Task(
        name=name,
        complete=False,
        user_id=current_user.id,
        due_date=due_date
    )
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('dashboard'))


@app.route('/update/<int:task_id>')
@login_required
def update(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if task:
        task.complete = not task.complete
        db.session.commit()
    return redirect(url_for('dashboard'))


@app.route('/delete/<int:task_id>')
@login_required
def delete(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('dashboard'))


@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()

    if request.method == 'POST':
        name = request.form.get("name")
        due_date_str = request.form.get("due_date")

        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash("Invalid date format. Use YYYY-MM-DD.", "error")
                return redirect(url_for('edit', task_id=task_id))

        if not name:
            flash("Task name cannot be empty.", "error")
            return redirect(url_for('edit', task_id=task_id))

        task.name = name
        task.due_date = due_date
        db.session.commit()
        flash("Task updated successfully!", "success")
        return redirect(url_for('dashboard'))

    return render_template('edit_task.html', task=task)


# ------------------ Run App ------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
