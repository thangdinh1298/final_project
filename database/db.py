from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from flask_login import UserMixin

engine = create_engine('mysql+pymysql://root:12345678@localhost:3306/CourseManager', echo=True)
Base = automap_base()

#Declare to inherit from UserMixin
#so we don't have to write our own is_authenticated method
class User(Base, UserMixin):
    __tablename__ = 'User'
    def __str__(self):
        return "{} {}".format(self.id, self.name)

Base.prepare(engine, reflect=True)
Session = sessionmaker(bind=engine)
Course = Base.classes.Course
Homework = Base.classes.Homework
StudyMaterial = Base.classes.StudyMaterial
Announcement = Base.classes.Announcement
UserCourse = Base.classes.UserCourse
