from flask import Blueprint, render_template, request
from database.db import Session, Course

course_page = Blueprint('simple_page', __name__,template_folder='templates')

@course_page.route('/course')
def course_handler():
    course_id = request.args.get('id')
    session = Session()
    course = session.query(Course).filter(Course.course_id==course_id).first()

    if course == None:
        return "Course not found"

    print("id: {} , name: {}".format(course.course_id, course.name))
    return render_template('course.html', course_name=course.name)

