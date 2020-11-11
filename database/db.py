from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://root:12345678@localhost:3306/CourseManager', echo=True)
Base = automap_base()
Base.prepare(engine, reflect=True)
Session = sessionmaker(bind=engine)
Course = Base.classes.Course
Homework = Base.classes.Homework
StudyMaterial = Base.classes.StudyMaterial
Announcement = Base.classes.Announcement
