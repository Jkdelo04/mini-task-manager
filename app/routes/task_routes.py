from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from ..models import Task
from ..extensions import db
from datetime import datetime, date

task_bp = Blueprint('task', __name__)

@task_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    query = Task.query.filter_by(user_id=current_user.id)

    # Filter options
    search_query = request.args.get('search', '')
    status_filter = request.args.get('status', 'all')
    sort_order = request.args.get('sort', 'asc')
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


@task_bp.route('/add', methods=['POST'])
@login_required
def add():
    name = request.form.get("name")
    due_date_str = request.form.get("due_date")

    due_date = None
    if due_date_str:
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        except ValueError:
            flash("Invalid date format. Use YYYY-MM-DD.", "error")

    new_task = Task(
        name=name,
        complete=False,
        user_id=current_user.id,
        due_date=due_date
    )
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('task.dashboard'))


@task_bp.route('/update/<int:task_id>')
@login_required
def update(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if task:
        task.complete = not task.complete
        db.session.commit()
    return redirect(url_for('task.dashboard'))


@task_bp.route('/delete/<int:task_id>')
@login_required
def delete(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('task.dashboard'))


@task_bp.route('/edit/<int:task_id>', methods=['GET', 'POST'])
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
                return redirect(url_for('task.edit', task_id=task_id))

        if not name:
            flash("Task name cannot be empty.", "error")
            return redirect(url_for('task.edit', task_id=task_id))

        task.name = name
        task.due_date = due_date
        db.session.commit()
        flash("Task updated successfully!", "success")
        return redirect(url_for('task.dashboard'))

    return render_template('edit_task.html', task=task)
