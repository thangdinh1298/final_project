from flask_login import LoginManager, login_user
from flask import Blueprint, request, redirect, url_for
from database.db import User, db

login_manager = LoginManager()
login_manager.login_view = "auth_page.login"
auth_page = Blueprint('auth_page', __name__)

@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        user = db.session.query(User).filter(User.id==user_id).first()
        print("User is: ", user)
        return user
    return None

@auth_page.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='username' id='username' placeholder='username'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               '''

    username = request.form['username']
    password = request.form['password']

    #FIXME: Hash password and compare
    user = db.session.query(User).filter(User.name==username, User.password==password).first()
    if user is not None:
        print("User is: ", user)
        login_user(user)
        return redirect(url_for('course_page.course_overview_handler', course_id=4))

    return '''
               <form action='login' method='POST'>
                <input type='text' name='username' id='username' placeholder='username'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               <div>Invalid credentials</div>
           '''
@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    return '<h2>Unauthorized</h2>'
