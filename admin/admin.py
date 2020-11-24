from flask import Blueprint, render_template, request, abort
from flask_login import login_required, current_user
from database.db import Course, db, User
from sqlalchemy.exc import SQLAlchemyError

admin_page = Blueprint('admin_page', __name__,template_folder='templates')

@admin_page.route('/course/', methods=['GET', 'POST'])
@login_required
def create_course_handler():
    if request.method == 'GET':
        return render_template('course/course_create_form.html') 
    
    name_msg = ""
    course_length_msg = ""
    owner_id_msg = ""
    if 'name' not in request.form:
        name_msg = "Please fill in a name"

    if 'course_length' not in request.form:
        course_length_msg = "Please choose a course length"

    if 'owner_id' not in request.form:
        owner_id_msg = "Please fill in an owner id"

    if name_msg != "" or course_length_msg != "" or owner_id_msg != "":
        return render_template('course/course_create_form.html', name_msg=name_msg\
                              , course_length_msg=course_length_msg\
                              , owner_id_msg=owner_id_msg)

    try:
        course = Course(name=request.form['name'], user_id=int(request.form['owner_id']))
        db.session.add(course)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        print(e)
        abort(500)
    except ValueError:
        abort(400)

    return "Successful"

@admin_page.url_value_preprocessor
def preprocessor(endpoint, values):
    if current_user.is_anonymous == True:
        abort(401)

    #2 is admin
    result = db.session.query(User.role).filter(User.id==current_user.id).first()
    if result == None:
        abort(401)

    if result.role != 2:
        abort(401)
