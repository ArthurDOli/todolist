from http.cookiejar import cut_port_re

from todolist import app, db, login_manager, bcrypt
from flask import render_template, request, redirect, url_for
from .forms import FormCreateTask, FormLogin, FormCreateAccount
from .models import Task, User
from flask_login import login_required, login_user, logout_user, current_user

@app.route('/', methods=['GET', 'POST'])
@login_required
def homepage():
    form = FormCreateTask()
    if form.validate_on_submit():
        task_name = form.text.data
        new_task = Task(name=task_name, user_id=current_user.id, is_done=False)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('homepage'))
    tasks = Task.query.all()
    return render_template('homepage.html', form=form, tasks=tasks)

@app.route('/delete/<int:task_id>', methods=['POST'])
@login_required
def delete(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id == current_user.id:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('homepage'))

@app.route('/edittask/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edittask(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        return redirect(url_for('homepage'))
    form = FormCreateTask()
    if form.validate_on_submit():
        task.name = form.text.data
        db.session.commit()
        return redirect(url_for('homepage'))
    elif request.method == 'GET':
        form.text.data = task.name
    return render_template('edit_task.html', form=form, task_id=task_id)

@app.route('/update_task/<int:task_id>', methods=['POST'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.is_done = bool(request.form.get('is_done'))
    db.session.commit()
    return redirect(url_for('homepage'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        user = User.query.filter_by(username=formlogin.username.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, formlogin.password.data):
            login_user(user)
            return redirect(url_for('homepage'))
    return render_template('login.html', form=formlogin)

@app.route('/account_creation', methods=['GET', 'POST'])
def account_creation():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    formaccount_creation = FormCreateAccount()
    if formaccount_creation.validate_on_submit():
        password_hashed = bcrypt.generate_password_hash(formaccount_creation.password.data).decode('utf-8')
        user = User(username=formaccount_creation.username.data, password_hash=password_hashed)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        return redirect(url_for('homepage'))
    return render_template('account_creation.html', form=formaccount_creation)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))