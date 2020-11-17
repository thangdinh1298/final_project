from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345678@localhost:3306/CourseManager'
db = SQLAlchemy(app)
Base = automap_base()

#Declare to inherit from UserMixin
#so we don't have to write our own is_authenticated method
class User(Base, UserMixin):
    __tablename__ = 'User'
    def __str__(self):
        return "{} {}".format(self.id, self.name)

Base.prepare(db.engine, reflect=True)
Course = Base.classes.Course
Homework = Base.classes.Homework
StudyMaterial = Base.classes.StudyMaterial
Announcement = Base.classes.Announcement
UserCourse = Base.classes.UserCourse
