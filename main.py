from flask import Flask
from controller.course import course_page

app = Flask(__name__)
app.register_blueprint(course_page)


if __name__ == "__main__":
    app.run(debug=True)
