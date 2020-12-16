from functools import wraps
from flask import Blueprint, render_template, request, Markup, session, abort, redirect, url_for, escape
from database.db import Course, Homework, StudyMaterial, Announcement, UserCourse, db
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError
from flask_login import login_required, current_user
from datetime import datetime
from app import app

course_page = Blueprint('course_page', __name__,template_folder='templates'\
                        ,static_folder='static')

def get_authorization(f):
    @wraps(f)
    def auth_func(*args, **kwargs):
        course_id = kwargs['course_id']
        result = db.session.query(UserCourse.id).filter(UserCourse.course_id==course_id, UserCourse.user_id==current_user.id).first()

        if result == None:
            return abort(401)
        
        return f(*args, **kwargs)
    return auth_func

def post_authorization(f):
    @wraps(f)
    def auth_func(*args, **kwargs):
        course_id = kwargs['course_id']
        result = db.session.query(Course.user_id).filter(Course.id==course_id).first()
        owner_id = result.user_id

        if owner_id != current_user.id:
            return abort(401)
        
        return f(*args, **kwargs)
    return auth_func

@course_page.route('/<int:course_id>/')
@login_required
@get_authorization
def view_course_handler(course_id=None):
    return redirect(url_for('.course_overview_handler', course_id=course_id))

@course_page.route('/<int:course_id>/overview')
@login_required
@get_authorization
def course_overview_handler(course_id=None):
    course = db.session.query(Course).filter(Course.id==course_id).first()
    course.description = Markup(course.description).unescape()
    return render_template('course/course_overview.html', course=course)

@course_page.route('/<int:course_id>/overview', methods=["POST", "DELETE"])
@login_required
@post_authorization
def course_overview_update_handler(course_id=None):
    course = db.session.query(Course).filter(Course.id==course_id).first()
    if request.method == "POST":
        description = request.form["description"]
        course.description = str(escape(description))

        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500)

        return "Successful"
    else:
        try:
            course.description = None
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500)

        return "Sucessful"

@course_page.route('/<int:course_id>/content')
@login_required
@get_authorization
def content_handler(course_id=None):
    course = db.session.query(Course.course_length).filter(Course.id==course_id).first()
    return render_template('course/course_content.html', course_length=course.course_length)

@course_page.route('/<int:course_id>/info')
@login_required
@get_authorization
def course_info_handler(course_id):
    course = db.session.query(Course.info).filter(Course.id==course_id).first()
    info = Markup(course.info).unescape()
    return render_template('course/course_info.html', info=info) 

@course_page.route('/<int:course_id>/info', methods=["POST", "DELETE"])
@login_required
@post_authorization
def course_info_update_handler(course_id):
    course = db.session.query(Course).filter(Course.id==course_id).first()
    if request.method == "POST":
        info = request.form["info"]
        course.info = str(escape(info))

        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500)

        return "Successful"
    else:
        try:
            course.info = None
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500)

        return "Sucessful"

@course_page.route('/<int:course_id>/week/<int:week_num>/homework')
@login_required
@get_authorization
def course_week_homework_handler(course_id=None,week_num=None):
    homework = db.session.query(Homework.description).filter(Homework.course_id==course_id, Homework.week==week_num).first()
    if homework == None:
        return render_template('course/course_content_detail.html')
    return render_template('course/course_content_detail.html', html=Markup(homework.description).unescape())

@course_page.route('/<int:course_id>/week/<int:week_num>/homework', methods=["POST", "DELETE"])
@login_required
@post_authorization
def course_week_homework_update_handler(course_id=None,week_num=None):
    homework = db.session.query(Homework).filter(Homework.course_id==course_id, Homework.week==week_num).first()
    if request.method == 'POST':
        if homework is None:
            homework = Homework(course_id=course_id, week=week_num, description=str(escape(request.form["homework"])))
            try:
                db.session.add(homework)
                db.session.commit()
            except SQLAlchemyError as e:
                db.session.rollback()
                abort(500)
        else:
            homework.description = str(escape(request.form['homework']))
            try:
                db.session.commit()
            except SQLAlchemyError as e:
                db.session.rollback()
                abort(500)

        return "Sucessful"
    else:
        if homework is None:
            return "Nothing to delete"
        else:
            try:
                db.session.delete(homework)
                db.session.commit()
            except SQLAlchemyError as e:
                db.session.rollback()
                abort(500)
            return "Sucessful"

@course_page.route('/<int:course_id>/week/<int:week_num>/material')
@login_required
@get_authorization
def course_week_material_handler(course_id=None,week_num=None):
    material = db.session.query(StudyMaterial.description).filter(StudyMaterial.course_id==course_id, StudyMaterial.week==week_num).first()
    if material == None: 
        return render_template('course/course_content_detail.html')
    return render_template('course/course_content_detail.html', html=Markup(material.description).unescape())

@course_page.route('/<int:course_id>/week/<int:week_num>/material', methods=["POST", "DELETE"])
@login_required
@post_authorization
def course_week_material_update_handler(course_id=None,week_num=None):
    material = db.session.query(StudyMaterial).filter(StudyMaterial.course_id==course_id, StudyMaterial.week==week_num).first()
    if request.method == "POST":
        if material is None:
            material = StudyMaterial(course_id=course_id, week=week_num, description=str(escape(request.form["material"])))
            try:
                db.session.add(material)
                db.session.commit()
            except SQLAlchemyError as e:
                db.session.rollback()
                abort(500)
        else:
            material.description = str(escape(request.form['material']))
            try:
                db.session.commit()
            except SQLAlchemyError as e:
                db.session.rollback()
                abort(500)

        return "Sucessful"
    else:
        if material is None:
            return "Nothing to delete"
        else:
            try:
                db.session.delete(material)
                db.session.commit()
            except SQLAlchemyError as e:
                db.session.rollback()
                abort(500)
            return "Sucessful"

@course_page.route('/<int:course_id>/livestream')
@login_required
@get_authorization
def course_livestream_handler(course_id=None):
    return render_template('course/course_livestream.html') 

@course_page.route('/<int:course_id>/announcements')
@login_required
@get_authorization
def course_announcements_handler(course_id=None):
    # FIXME: Perhaps we need no fetch by pages and not all...
    announcements = db.session.query(Announcement).filter(Announcement.course_id==course_id).order_by(desc(Announcement.created_date)).all()
    for announcement in announcements:
        announcement.description = Markup(announcement.description).unescape()
    return render_template('course/course_announcements.html', announcements=announcements)

@course_page.route('/<int:course_id>/announcements', methods=["POST"])
@login_required
@post_authorization
def course_announcements_create_handler(course_id=None):
    course = db.session.query(Course).filter(Course.id==course_id).first()
    announcement = Announcement(description=str(escape(request.form["announcement"])), course_id=course_id, created_date=datetime.today())

    try:
        db.session.add(announcement)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(500)
    return "Successful"

@course_page.route('/<int:course_id>/update_page')
@login_required
@post_authorization
def course_update_page_handler(course_id=None):
    course = db.session.query(Course).filter(Course.id==course_id).first()
    announcements = db.session.query(Announcement).filter(Announcement.course_id==course_id).order_by(desc(Announcement.created_date)).limit(2).all()
    course.description = Markup(course.description).unescape() if course.description is not None else None
    course.info = Markup(course.info).unescape() if course.info is not None else None

    for announcement in announcements:
        announcement.description = Markup(announcement.description).unescape()

    return render_template("course/course_update_page.html", course=course, announcements=announcements)

@course_page.route('/<int:course_id>/week/<int:week_num>/update_page')
@login_required
@post_authorization
def course_week_update_handler(course_id=None, week_num=None):
    material = db.session.query(StudyMaterial.description).filter(StudyMaterial.course_id==course_id, StudyMaterial.week==week_num).first()
    homework = db.session.query(Homework.description).filter(Homework.course_id==course_id, Homework.week==week_num).first()
    context = {}
    if material is not None:
        context['material'] = Markup(material.description).unescape()
    if homework is not None:
        context['homework'] = Markup(homework.description).unescape()
    context['week'] = week_num

    return render_template("course/course_week_content_update.html", context=context)

@course_page.url_value_preprocessor
def set_course_id(endpoint, values):
    if 'course_id' not in values:
        abort(404)
    course_id = values['course_id']
    if db.session.query(Course.id).filter(Course.id==course_id).first() == None:
        abort(404)

    session['course_id'] = values['course_id']
