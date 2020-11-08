from flask import Blueprint, render_template, request, Markup
from database.db import Session, Course

course_page = Blueprint('simple_page', __name__,template_folder='templates')

@course_page.route('/')
def course_overview_handler():
    course_id = request.args.get('course_id')
    session = Session()
    course = session.query(Course).filter(Course.id==course_id).first()

    if course == None:
        return "Course not found"

    print("id: {} , name: {}".format(course.id, course.name))
    return render_template('course.html', course=course)

@course_page.route('/hello')
def hello_handler():
    return "course id is: {}".format(request.args.get('course_id'))

@course_page.route('info')
def course_info_handler():
    course_id = request.args.get('course_id')
    session = Session()
    course = session.query(Course.info).filter(Course.id==course_id).first()

    if course == None:
        return "Course not found"
    return Markup(course.info).unescape()
