from flask import Blueprint, render_template, request, abort
from flask_login import login_required, current_user
from database.db import Course, db
from sqlalchemy.exc import SQLAlchemyError

admin_page = Blueprint('admin_page', __name__,template_folder='templates')

@admin_page.route('/course/', methods=['GET', 'POST'])
@login_required
def create_course_handler():
    if request.method == 'GET':
        return render_template('course/course_create_form.html') 
    
    name_msg = ""
    course_length_msg = ""
    if 'name' not in request.form:
        name_msg = "Please fill in a name"

    if 'course_length' not in request.form:
        course_length_msg = "Please choose a course length"

    if name_msg != "" or course_length_msg != "":
        return render_template('course/course_create_form.html', name_msg=name_msg\
                              , course_length_msg=course_length_msg)

    try:
        course = Course(name=request.form['name'], user_id=1)
        db.session.add(course)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        print(e)
        abort(500)
    return "Successful"
