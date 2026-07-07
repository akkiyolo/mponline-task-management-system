import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# ---------------------------------------------------------------------------
# App Configuration
# ---------------------------------------------------------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'task-manager-secret-key-2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------
class Admin(UserMixin, db.Model):
    """Admin user model for authentication."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Task(db.Model):
    """Task model – PK auto-increment, as shown in the architecture."""
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_name = db.Column(db.String(120), nullable=False)
    task_title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'task_id': self.task_id,
            'employee_name': self.employee_name,
            'task_title': self.task_title,
            'completed': self.completed,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M') if self.updated_at else None
        }


@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

# ---------------------------------------------------------------------------
# Routes – Authentication
# ---------------------------------------------------------------------------
@app.route('/')
def index():
    """Redirect root to login if not authenticated, else dashboard."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            login_user(admin)
            flash('Welcome back, Admin!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'error')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

# ---------------------------------------------------------------------------
# Routes – Dashboard & Tasks
# ---------------------------------------------------------------------------
@app.route('/dashboard')
@login_required
def dashboard():
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    total = Task.query.count()
    completed = Task.query.filter_by(completed=True).count()
    pending = total - completed
    return render_template('dashboard.html',
                           tasks=tasks,
                           total=total,
                           completed=completed,
                           pending=pending)


@app.route('/tasks/add', methods=['POST'])
@login_required
def add_task():
    employee_name = request.form.get('employee_name', '').strip()
    task_title = request.form.get('task_title', '').strip()
    completed = request.form.get('completed') == 'true'

    if not employee_name or not task_title:
        flash('Employee name and task title are required.', 'error')
        return redirect(url_for('dashboard'))

    task = Task(employee_name=employee_name,
                task_title=task_title,
                completed=completed)
    db.session.add(task)
    db.session.commit()
    flash(f'Task #{task.task_id} created successfully!', 'success')
    return redirect(url_for('dashboard'))


@app.route('/tasks/edit/<int:task_id>', methods=['POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.employee_name = request.form.get('employee_name', task.employee_name).strip()
    task.task_title = request.form.get('task_title', task.task_title).strip()
    task.completed = request.form.get('completed') == 'true'
    db.session.commit()
    flash(f'Task #{task.task_id} updated successfully!', 'success')
    return redirect(url_for('dashboard'))


@app.route('/tasks/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash(f'Task #{task_id} deleted.', 'info')
    return redirect(url_for('dashboard'))


@app.route('/tasks/toggle/<int:task_id>', methods=['POST'])
@login_required
def toggle_task(task_id):
    """AJAX endpoint to toggle completed status."""
    task = Task.query.get_or_404(task_id)
    task.completed = not task.completed
    db.session.commit()
    return jsonify(task.to_dict())

# ---------------------------------------------------------------------------
# Database Initialisation & Default Admin
# ---------------------------------------------------------------------------
def init_db():
    """Create tables and seed a default admin if none exists."""
    with app.app_context():
        db.create_all()
        if not Admin.query.first():
            admin = Admin(username='admin')
            admin.set_password('admin')
            db.session.add(admin)
            db.session.commit()
            print('[OK] Default admin created -> username: admin | password: admin')

# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
