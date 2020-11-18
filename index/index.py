from flask import Blueprint, render_template, request, Markup, session, abort
from flask_login import login_required, current_user

index_page = Blueprint('index_page', __name__,template_folder='templates')

@index_page.route('/index')
@login_required
def index_page_handler():
    return render_template('index.html')

@index_page.route('/dummy')
@login_required
def dummy_handler():
    return "Hello"
