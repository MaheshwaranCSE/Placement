from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField, SelectField, TextAreaField, MultipleFileField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional, Regexp, ValidationError
from backend.models.student import Student

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=64)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=10, message="Password must be at least 10 characters long."),
        Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{10,}$',
               message="Password must contain at least one uppercase letter, one number, and one special character.")
    ])
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        # Use custom validation logic if importing EqualTo is an issue or ensure standard EqualTo
    ])
    submit = SubmitField('Change Password')

    def validate_confirm_password(self, field):
        if field.data != self.new_password.data:
            raise ValidationError('Passwords must match.')

class StudentForm(FlaskForm):
    roll_number = StringField('Roll Number', validators=[DataRequired(), Length(max=20)])
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[Optional(), Email(), Length(max=120)])
    department = SelectField('Department', choices=[
        ('CSE', 'Computer Science'),
        ('ECE', 'Electronics'),
        ('MECH', 'Mechanical'),
        ('CIVIL', 'Civil'),
        ('IT', 'Information Technology')
    ], validators=[DataRequired()])
    batch_year = IntegerField('Batch Year', validators=[DataRequired(), NumberRange(min=2000, max=2100)])
    cgpa = FloatField('CGPA', validators=[DataRequired(), NumberRange(min=0.0, max=10.0)])
    backlogs = IntegerField('Backlogs', validators=[Optional(), NumberRange(min=0)])
    internships = IntegerField('Internships', validators=[Optional(), NumberRange(min=0)])
    projects = IntegerField('Projects', validators=[Optional(), NumberRange(min=0)])
    skills = StringField('Skills (comma separated)', validators=[Optional()])
    communication_score = IntegerField('Communication Score (0-10)', validators=[Optional(), NumberRange(min=0, max=10)])
    aptitude_score = IntegerField('Aptitude Score (0-10)', validators=[Optional(), NumberRange(min=0, max=10)])
    extra_curricular = TextAreaField('Extra Curricular Activities', validators=[Optional()])
    linkedin_url = StringField('LinkedIn URL', validators=[Optional(), Length(max=200)])
    github_url = StringField('GitHub URL', validators=[Optional(), Length(max=200)])
    resume = FileField('Resume (PDF)', validators=[Optional(), FileAllowed(['pdf'], 'PDFs only!')])
    submit = SubmitField('Save Student')

class PlacementForm(FlaskForm):
    company = StringField('Company', validators=[DataRequired(), Length(max=100)])
    role_offered = StringField('Role Offered', validators=[Optional(), Length(max=100)])
    offer_date = StringField('Offer Date (YYYY-MM-DD)', validators=[Optional()])
    joining_date = StringField('Joining Date (YYYY-MM-DD)', validators=[Optional()])
    package_lpa = FloatField('Package (LPA)', validators=[Optional(), NumberRange(min=0)])
    location = StringField('Location', validators=[Optional(), Length(max=100)])
    status = SelectField('Status', choices=[
        ('placed', 'Placed'),
        ('not_placed', 'Not Placed'),
        ('waiting', 'Waiting List'),
        ('internship', 'Internship'),
        ('ppo', 'Pre-Placement Offer'),
        ('rejected', 'Rejected')
    ], validators=[DataRequired()])
    notes = TextAreaField('Notes', validators=[Optional()])
    submit = SubmitField('Save Placement Record')

class ImportForm(FlaskForm):
    file = FileField('CSV/Excel File', validators=[
        DataRequired(),
        FileAllowed(['csv', 'xlsx', 'xls'], 'CSV or Excel files only!')
    ])
    submit = SubmitField('Import Students')
