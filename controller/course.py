from flask import Blueprint, render_template, request, Markup, session, abort
from database.db import Session, Course, Homework, StudyMaterial, Announcement
from sqlalchemy import desc
from flask_login import login_required

course_page = Blueprint('course_page', __name__,template_folder='templates')

@course_page.route('/<int:course_id>')
@login_required
def course_overview_handler(course_id=None):
    db_session = Session()
    course = db_session.query(Course).filter(Course.id==course_id).first()

    if course == None:
        abort(404)

    return render_template('course_overview.html', course=course)

@course_page.route('/<int:course_id>/content')
@login_required
def content_handler(course_id=None):
    db_session = Session()
    course = db_session.query(Course.course_length).filter(Course.id==course_id).first()

    if course == None:
        abort(404)

    return render_template('course_content.html', course_length=course.course_length)

@course_page.route('/<int:course_id>/info')
@login_required
def course_info_handler(course_id):
    db_session = Session()
    course = db_session.query(Course.info).filter(Course.id==course_id).first()

    if course == None:
        abort(404)
    info = Markup(course.info).unescape()
    return render_template('course_info.html', info=info) 

@course_page.route('/<int:course_id>/week/<int:week_num>/homework')
@login_required
def course_week_homework_handler(course_id=None,week_num=None):
    db_session = Session()
    homework = db_session.query(Homework.description).filter(Homework.course_id==course_id, Homework.week==week_num).first()
    if homework == None:
        abort(404)
    return render_template('course_content_detail.html', html=homework.description)

@course_page.route('/<int:course_id>/week/<int:week_num>/material')
@login_required
def course_week_material_handler(course_id=None,week_num=None):
    db_session = Session()
    material = db_session.query(StudyMaterial.description).filter(StudyMaterial.course_id==course_id, StudyMaterial.week==week_num).first()
    if material == None: 
        abort(404)
    return render_template('course_content_detail.html', html=material.description)

@course_page.route('/<int:course_id>/livestream')
@login_required
def course_livestream_handler(course_id=None):
    return render_template('course_livestream.html') 

@course_page.route('/<int:course_id>/announcements')
@login_required
def course_announcements_handler(course_id=None):
    db_session = Session()
    # FIXME: Perhaps we need no fetch by pages and not all...
    announcements = db_session.query(Announcement.description, Announcement.created_date).filter(Announcement.course_id==course_id).order_by(desc(Announcement.created_date)).all()
    return render_template('course_announcements.html', announcements=announcements)

@course_page.url_value_preprocessor
def set_course_id(endpoint, values):
    if 'course_id' not in values:
        abort(404)
    session['course_id'] = values['course_id']
