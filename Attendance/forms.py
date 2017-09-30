from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, Optional


class NameForm(FlaskForm):
    """
    Generic form for getting names and emails.

    This form contains name and email fields and serves as a base form for others to build upon.
    """
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[Email(), Optional()])


class EditTutorForm(NameForm):
    '''
    This form is for the Edit Tutor functionality of the app.

    '''
    user = SelectField('User', validators = [Optional()], coerce=int)


class EditStudentForm(NameForm):
    '''
        This form is for the Edit Student functionality of the app.

        University and College are optional for the time being as they are currently not coded into the app.
    '''
    studentcode = StringField('Student Code', validators=[Optional()])
    university = SelectField('University', validators=[Optional()],
                             choices=[("", ""), ('University of Melbourne', 'University of Melbourne'),
                                      ('RMIT', 'RMIT'), ('Monash', 'Monash')])
    college = SelectField('College', validators=[Optional()],
                          choices=[("", ""), ('International House', 'International House'), ('Whitley', 'Whitley')])

class LoginForm(FlaskForm):
    '''
    This is the login form used by Flask-login for registration and logging in.
    '''
    user_id = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class AddSubjectForm(FlaskForm):
    '''
    Form used to add subjects.
    '''
    subcode = StringField('Subject Code', validators=[DataRequired()])
    subname = StringField('Subject Name', validators=[DataRequired()])


class StudentForm(NameForm):
    studentcode = StringField('Student Code', validators=[DataRequired()])


class AddTimetableForm(FlaskForm):
    key = StringField('Timetable Name', validators=[DataRequired()])


class TimeslotForm(FlaskForm):
    day = StringField('Day', validators=[DataRequired()])
    time = StringField('Time', validators=[DataRequired()])


class JustNameForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
