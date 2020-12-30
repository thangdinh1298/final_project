from flask_login import LoginManager, login_user, logout_user, login_required
from flask import Blueprint, request, redirect, url_for, render_template
from database.db import User, db

login_manager = LoginManager()
login_manager.login_view = "auth_page.login"
auth_page = Blueprint('auth_page', __name__, template_folder='templates', static_folder='static')

@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        user = db.session.query(User).filter(User.id==user_id).first()
        return user
    return None

@auth_page.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')

    username = request.form['username']
    password = request.form['password']

    #FIXME: Hash password and compare
    user = db.session.query(User).filter(User.username==username, User.password==password).first()
    if user is not None:
        login_user(user)
        return redirect(url_for('index_page.index_page_handler'))

    return render_template('auth/login.html')
@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    return '<h2>Unauthorized</h2>'

@auth_page.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('.login'))

