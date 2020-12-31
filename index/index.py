from flask import Blueprint, render_template, request, url_for
from flask_login import login_required, current_user
from database.db import db, Course, UserCourse

index_page = Blueprint('index_page', __name__,template_folder='templates')
RESULT_PER_PAGE = 2

#TODO: Make default page your courses page
@index_page.route('/index')
@login_required
def index_page_handler():
    return render_template('index/index.html')

@index_page.route('/find_courses', methods=['GET'])
@login_required
def find_courses_handler():
    if 'q' not in request.args or request.args['q'] == "":
        return render_template('index/find_course.html')

    page = request.args.get('page', 1, type=int)
    text = request.args['q'] 
    search_pattern = '%{}%'.format(text)
    courses = db.session.query(Course.id, Course.name)\
                        .filter(Course.name.like(search_pattern))\
                        .paginate(page, RESULT_PER_PAGE, False)
    next_url = url_for('.find_courses_handler', page=courses.next_num, q=text)\
            if courses.has_next else None
    prev_url = url_for('.find_courses_handler', page=courses.prev_num, q=text)\
            if courses.has_prev else None
    return render_template('index/find_course.html', search_result=courses.items,\
                            next_url=next_url, prev_url=prev_url)

@index_page.route('/view_registered_courses')
@login_required
def view_registered_courses_handler():
    page = request.args.get('page', 1, type=int)
    courses = db.session.query(Course.id, Course.name).join(UserCourse, Course.id==UserCourse.course_id).filter(UserCourse.user_id==current_user.id).paginate(page, RESULT_PER_PAGE, False)
    next_url = url_for('.view_registered_courses_handler', page=courses.next_num)\
            if courses.has_next else None
    prev_url = url_for('.view_registered_courses_handler', page=courses.prev_num)\
            if courses.has_prev else None
    return render_template('index/view_registered_course.html', courses=courses.items,\
                            next_url=next_url, prev_url=prev_url)

@index_page.route('/view_owned_courses')
@login_required
def view_owned_courses_handler():
    page = request.args.get('page', 1, type=int)
    courses = db.session.query(Course.id, Course.name).filter(Course.user_id==current_user.id).paginate(page, RESULT_PER_PAGE, False)
    next_url = url_for('.view_owned_courses_handler', page=courses.next_num)\
            if courses.has_next else None
    prev_url = url_for('.view_owned_courses_handler', page=courses.prev_num)\
            if courses.has_prev else None
    return render_template('index/view_owned_courses.html', courses=courses.items,\
                            next_url=next_url, prev_url=prev_url)


@index_page.route('/statistics')
@login_required
def view_statistics_handler():
    num_course_owned = db.session.query(Course.id).filter(Course.user_id == current_user.id).all()
    courses = [course.id for course in num_course_owned]
    num_participants = db.session.query(UserCourse).filter(UserCourse.course_id.in_(courses)).count()
    num_course_participated = db.session.query(UserCourse).filter(UserCourse.user_id==current_user.id).count()
    return render_template('index/statistics.html', num_course_owned=len(num_course_owned), num_participants=num_participants, num_course_participated=num_course_participated)
