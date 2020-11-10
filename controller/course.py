from flask import Blueprint, render_template, request, Markup, session
from database.db import Session, Course, Homework, StudyMaterial

course_page = Blueprint('course_page', __name__,template_folder='templates')

@course_page.route('/<int:course_id>')
def course_overview_handler(course_id=None):
    if course_id == None:
        return "Course not found"
    session['course_id'] = course_id

    db_session = Session()
    course = db_session.query(Course).filter(Course.id==course_id).first()

    if course == None:
        return "Course not found"

    return render_template('course_overview.html', course=course)

@course_page.route('/hello')
def hello_handler():
    return "course id is: {}".format(request.args.get('course_id'))

@course_page.route('/<int:course_id>/content')
def content_handler(course_id=None):
    if course_id == None:
        return "Course not found"
    session['course_id'] = course_id

    db_session = Session()
    course = db_session.query(Course.course_length).filter(Course.id==course_id).first()

    if course == None:
        return "Course not found"

    return render_template('course_content.html', course_length=course.course_length)

@course_page.route('/<int:course_id>/info')
def course_info_handler(course_id):
    if course_id == None:
        return "Course not found"
    session['course_id'] = course_id

    db_session = Session()
    course = db_session.query(Course.info).filter(Course.id==course_id).first()

    if course == None:
        return "Course not found"
    info = Markup(course.info).unescape()
    return render_template('course_info.html', info=info) 

@course_page.route('/<int:course_id>/week/<int:week_num>/homework')
def course_week_homework_handler(course_id=None,week_num=None):
    db_session = Session()
    homework = db_session.query(Homework.description).filter(Homework.course_id==course_id, Homework.week==week_num).first()
    if homework == None:
        return "Resource not found"
    return render_template('course_content_detail.html', html=homework.description)

@course_page.route('/<int:course_id>/week/<int:week_num>/material')
def course_week_material_handler(course_id=None,week_num=None):
    db_session = Session()
    material = db_session.query(StudyMaterial.description).filter(StudyMaterial.course_id==course_id, StudyMaterial.week==week_num).first()
    if material == None: 
        return "Resource not found"
    return render_template('course_content_detail.html', html=material.description)

@course_page.route('/<int:course_id>/livestream')
def course_livestream_handler(course_id=None):
    pass 
