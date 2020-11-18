from app import app
from os import urandom
from flask import render_template, redirect, url_for
from course.course import course_page
from auth.auth import login_manager, auth_page
from index.index import index_page


login_manager.init_app(app)
app.secret_key = urandom(24)
app.register_blueprint(course_page, url_prefix='/course')
app.register_blueprint(auth_page)
app.register_blueprint(index_page)

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.register_error_handler(404, page_not_found)
    app.run(debug=True)
