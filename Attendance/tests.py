import unittest
import abc
from pandas import DataFrame
from flask import Flask
from Attendance import db
from Attendance.models import *
from Attendance.views import *


class BaseTest(unittest.TestCase):
    '''
    This class takes in the common setup and teardown methods. This means that
    we don't have to repeat ourselves and we can just put any inital stuff for a class
    in the setUpTestData method.

    '''
    __metaclass__ = abc.ABCMeta

    def setUp(self):
        self.app = Flask(__name__)
        # self.app.config['SQLALCHEMY_DATABASE_URI']='sqlite:////'
        db.init_app(self.app)
        db.session.remove()
        db.drop_all()
        db.create_all()
        populate_admin_table()
        self.setUpTestData()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    @abc.abstractmethod
    def setUpTestData(self):
        return

class StudentTests(BaseTest):
    # Create student for the test
    def setUpTestData(self):
        student = Student.create(name='Justin Smallwood', studentcode=542066)

    def test_get(self):
        student = Student.get(name="Justin Smallwood")
        self.assertTrue(isinstance(student, Student))
        self.assertEqual(student.name, "Justin Smallwood")

    def test_update(self):
        newname = "Jemima Capper"
        student = Student.get(name="Justin Smallwood")
        student.update(name=newname)
        self.assertEqual(student.name, newname)

    def test_delete(self):
        student = Student.get(name='Justin Smallwood')
        student = Student.get(name="Justin Smallwood")
        student.delete()
        self.assertEqual(Student.get(name="Justin Smallwood"), None)

    def test_populate_students(self):
        data = DataFrame(columns=['Given Name', 'Family Name', 'Student Id', 'Component Study Package Code',
                                  'Component Study Package Title', 'Study Period'])
        data['Given Name'] = ['Justin', 'Jemima']
        data['Family Name'] = ['Smallwood', 'Capper']
        data['Student Id'] = ['542066', '356351']
        data['Component Study Package Code'] = ['ECON10005', 'ECON20003']
        data['Component Study Package Title'] = ['Quantitative Methods 1', 'Quantitative Methods 2']
        data['Study Period'] = [get_current_studyperiod() for i in range(2)]
        populate_students(data)
        student = Student.get(name='Justin Smallwood')
        subject = Subject.get(subcode='ECON10005')
        self.assertEqual(student.name, 'Justin Smallwood')
        self.assertTrue(isinstance(student, Student))
        self.assertEqual(subject.subname, 'Quantitative Methods 1')
        self.assertTrue(isinstance(subject, Subject))
        self.assertIsNotNone(student)
        self.assertIsNotNone(subject)
        self.assertIn(subject, student.subjects)
        self.assertIn(student, subject.students)
        student = Student.get(name='Jemima Capper')
        subject = Subject.get(subcode='ECON20003')
        self.assertEqual(student.name, 'Jemima Capper')
        self.assertTrue(isinstance(student, Student))
        self.assertEqual(subject.subname, 'Quantitative Methods 2')
        self.assertTrue(isinstance(subject, Subject))
        self.assertIsNotNone(student)
        self.assertIsNotNone(subject)
        self.assertIn(subject, student.subjects)
        self.assertIn(student, subject.students)



class SubjectTests(BaseTest):
    def setUpTestData(self):
        # Create subject for the test
        subject = Subject.create(subcode='ECON10005', subname='Quantitative Methods 1')

    def test_get(self):
        subject = Subject.get(subcode="ECON10005")
        self.assertTrue(isinstance(subject, Subject))
        self.assertEqual(subject.subname, "Quantitative Methods 1")

    def test_update(self):
        newname = "Quantitative Methods 2"
        subject = Subject.get(subcode="ECON10005")
        subject.update(subname=newname)
        self.assertEqual(subject.subname, newname)

    def test_delete(self):
        subject = Subject.get(subcode="ECON10005")
        self.assertEqual(subject.subname, "Quantitative Methods 1")
        subject.delete()
        self.assertEqual(Subject.get(subcode="ECON10005"), None)


class UserTests(BaseTest):
    def setUpTestData(self):
        User.create(username='testuser', password='testuser')

    def test_get(self):
        user = User.get(username="testuser")
        self.assertTrue(isinstance(user, User))
        self.assertIsNotNone(user)


class AdminTests(BaseTest):
    def setUpTestData(self):
        return True

    def test_update_year(self):
        year = int(get_current_year()) + 1
        update_year(year)
        self.assertEqual(year, get_current_year())

    def test_update_studyperiod(self):
        studyperiod = "TEST STUDY PERIOD"
        update_studyperiod(studyperiod)
        self.assertEqual(studyperiod, get_current_studyperiod())


class TimeslotTests(BaseTest):
    def setUpTestData(self):
        return True

    def test_add_timeslot(self):
        day = "Monday"
        time = "7:30pm"
        Timeslot.get_or_create(day=day, time=time)
        self.assertIsNotNone(Timeslot.get(day=day, time=time))


class TimetableTests(BaseTest):
    def test_timetable(self):
        Student.create(name='Justin Smallwood', studentcode=542066)
        Student.create(name='Tom Cox', studentcode=123595)
        Subject.create(subcode='ECON10005', subname='Quantitative Methods 1', repeats=1)
        Subject.create(subcode='MAST10006', subname='Calculus 2', repeats=1)
        STUDENTS = ['Justin Smallwood', 'Tom Cox']
        SUBJECTS = ['ECON10005', 'MAST10006']
        Timeslot.create(day='Monday', time='7:30pm')
        Timeslot.create(day='Tuesday', time='9:30pm')
        TIMES = ['Monday 7:30pm', 'Tuesday 9:30pm']
        day = ['Monday', 'Tuesday']
        DAYS = {}
        DAYS['Monday'] = ['Monday 7:30pm']
        DAYS['Tuesday'] = ['Tuesday 9:30pm']
        tutor = Tutor.get_or_create(name='Omid Kaveh')
        tutor.subjects.append(Subject.get(subcode='MAST10006'))
        db.session.commit()
        tutor = Tutor.get_or_create(name='Jemima Capper')
        tutor.subjects.append(Subject.get(subcode='ECON10005'))
        db.session.commit()
        TEACHERS = ['Omid Kaveh', 'Jemima Capper']
        REPEATS = {}
        REPEATS['ECON10005'] = 1
        REPEATS['MAST10006'] = 1
        maxclasssize = 2
        minclasssize = 1
        nrooms = 12
        TEACHERMAPPING = {}
        TEACHERMAPPING['Omid Kaveh'] = ['MAST10006']
        TEACHERMAPPING['Jemima Capper'] = ['ECON10005']
        TUTORAVAILABILITY = {}
        TUTORAVAILABILITY['Omid Kaveh'] = ['Monday 7:30pm']
        TUTORAVAILABILITY['Jemima Capper'] = ['Monday 7:30pm', 'Tuesday 9:30pm']
        SUBJECTMAPPING = {}
        SUBJECTMAPPING['ECON10005'] = ['Justin Smallwood', 'Tom Cox']
        student = Student.get(name='Tom Cox')
        student.subjects.append(Subject.get(subcode='ECON10005'))
        SUBJECTMAPPING['MAST10006'] = ['Justin Smallwood']
        student = Student.get(name='Justin Smallwood')
        student.subjects.append(Subject.get(subcode='MAST10006'))
        student.subjects.append(Subject.get(subcode='ECON10005'))

        result = runtimetable(STUDENTS, SUBJECTS, TIMES, day, DAYS, TEACHERS, SUBJECTMAPPING, REPEATS, TEACHERMAPPING,
                              TUTORAVAILABILITY, maxclasssize, minclasssize, nrooms)
        self.assertEqual(result, 'Optimal')


class TestHelpers(BaseTest):
    def test_checkbox(self):
        checkbox = None
        result = checkboxvalue(checkbox)
        self.assertEqual(result, 0)
        checkbox = 1
        result = checkboxvalue(checkbox)
        self.assertEqual(result, 1)


class TestViews(BaseTest):
    def setUpTestData(self):
        student = Student.get_or_create(name='Justin Smallwood', studentcode=542066)
        subject = Subject.get_or_create(subcode='ECON10005', subname='Quantitative Methods 1', repeats=1)

def populate_admin_table():
    if Admin.query.filter_by(key='currentyear').first() == None:
        admin = Admin(key='currentyear', value=2017)
        db.session.add(admin)
        db.session.commit()
    if Admin.query.filter_by(key='studyperiod').first() == None:
        study = Admin(key='studyperiod', value='Semester 2')
        db.session.add(study)
        db.session.commit()
    if Admin.query.filter_by(key='timetable').first() is None:
        timetable = Timetable(key="default")
        db.session.add(timetable)
        db.session.commit()
        timetableadmin = Admin(key='timetable', value=timetable.id)
        db.session.add(timetableadmin)
        db.session.commit()
