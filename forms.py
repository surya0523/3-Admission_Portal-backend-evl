from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField
# Import required validators
from wtforms.validators import DataRequired, Email, Length, ValidationError
# NOTE: We removed the direct Applicant model import to avoid the RuntimeError

class RegistrationForm(FlaskForm):
    full_name = StringField('Full Name', 
                            validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', 
                        # 'Email' validator requires the 'email_validator' package
                        validators=[DataRequired(), Email()]) 
    phone_number = StringField('Phone Number', 
                               validators=[DataRequired(), Length(max=20)])
    program = SelectField('Program Applying For', 
                          choices=[('CS', 'Computer Science'), ('EE', 'Electrical Eng.'), ('BA', 'Business Admin')], 
                          validators=[DataRequired()])
    submit = SubmitField('Register')
    
    # NOTE: The custom validate_email function was REMOVED to fix the RuntimeError.
    # Email uniqueness check is now handled in routes.py (inside the app context).

class AdminLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    
class AdminApprovalForm(FlaskForm):
    status = SelectField('New Status', 
                         choices=[('Approved', 'Approved'), ('Rejected', 'Rejected'), ('Pending', 'Pending')], 
                         validators=[DataRequired()])
    submit = SubmitField('Update Status')