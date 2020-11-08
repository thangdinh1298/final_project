from flask import Blueprint, render_template, request, Markup, session
from database.db import Session, Course

course_page = Blueprint('simple_page', __name__,template_folder='templates')

'''
This function returns the appropriate course_id for the request.
It checks in the session object if an id hasn't been provided as
a parameter.
'''
def set_session_and_get_course(request):
    course_id = None
    if 'course_id' in request.args:
        course_id = request.args.get('course_id')
        session['course_id'] = course_id
    elif 'course_id' in session:
        course_id = session['course_id']
    return course_id


@course_page.route('/')
def course_overview_handler():
    course_id = set_session_and_get_course(request)
    if course_id == None:
        return "Course not found"

    db_session = Session()
    course = db_session.query(Course).filter(Course.id==course_id).first()

    if course == None:
        return "Course not found"

    return render_template('course_overview.html', course=course)

@course_page.route('/hello')
def hello_handler():
    return "course id is: {}".format(request.args.get('course_id'))

@course_page.route('/content')
def content_handler():
    course_id = set_session_and_get_course(request)
    if course_id == None:
        return "Course not found"

    db_session = Session()
    course = db_session.query(Course.course_length).filter(Course.id==course_id).first()

    if course == None:
        return "Course not found"

    return render_template('course_content.html', course_length=course.course_length)

@course_page.route('info')
def course_info_handler():
    course_id = set_session_and_get_course(request)
    if course_id == None:
        return "Course not found"

    db_session = Session()
    course = db_session.query(Course.info).filter(Course.id==course_id).first()

    if course == None:
        return "Course not found"
    info = Markup(course.info).unescape()
    return render_template('course_info.html', info=info) 

@course_page.route('week')
def course_week_handler():
    return "Hello World"
