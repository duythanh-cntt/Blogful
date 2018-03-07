from project import app
from flask import render_template, redirect
from flask_login import login_required, current_user


@app.route('/admin/')
@login_required
def admin():
    account = current_user.username
    return render_template('back-end/_index.html', account=account)