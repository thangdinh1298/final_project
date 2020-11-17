from app import app
from flask_login import  logout_user, login_required
from flask import render_template, redirect, url_for
from controller.course import course_page
from controller.auth import login_manager, auth_page


login_manager.init_app(app)
app.secret_key = '123'
app.register_blueprint(course_page, url_prefix='/course')
app.register_blueprint(auth_page)

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_page.login'))


if __name__ == "__main__":
    app.register_error_handler(404, page_not_found)
    app.run(debug=True)
