from flask import Blueprint, render_template, request, url_for
from flask_login import login_required, current_user
from database.db import db, Course, UserCourse

index_page = Blueprint('index_page', __name__,template_folder='templates')
RESULT_PER_PAGE = 1

#TODO: Make default page your courses page
@index_page.route('/index')
@login_required
def index_page_handler():
    return render_template('index/index.html')

@index_page.route('/dummy')
@login_required
def dummy_handler():
    return "Hello"

@index_page.route('/find_courses')
@login_required
def find_course_handler():
    if request.method == 'GET':
        return render_template('index/find_course.html')

@index_page.route('/view_registered_courses')
@login_required
def view_registered_courses_handler():
    page = request.args.get('page', 1, type=int)
#    courses = db.session.query(Course).paginate(page, result_per_page, False)
    courses = db.session.query(Course.id, Course.name).join(UserCourse, Course.id==UserCourse.course_id).filter(UserCourse.user_id==current_user.id).paginate(page, RESULT_PER_PAGE, False)
    next_url = url_for('.view_registered_courses_handler', page=courses.next_num)\
            if courses.has_next else None
    prev_url = url_for('.view_registered_courses_handler', page=courses.prev_num)\
            if courses.has_prev else None
    return render_template('index/view_registered_course.html', courses=courses.items,\
                            next_url=next_url, prev_url=prev_url)

#TODO: Create request should be submitted to the course blueprint, not this
@index_page.route('/create')
@login_required
def create_course_handler():
    return "Hello"
