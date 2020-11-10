from flask import Flask, render_template
from controller.course import course_page

app = Flask(__name__)
app.secret_key = '123'
app.register_blueprint(course_page, url_prefix='/course')

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.register_error_handler(404, page_not_found)
    app.run(debug=True)
