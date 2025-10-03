from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from forms import RegistrationForm, AdminLoginForm, AdminApprovalForm
from models import Applicant, AdminUser, db
from utils import send_email_notification, send_sms_notification 
import secrets
from functools import wraps

main = Blueprint('main', __name__)

# --- UTILITY: Simple Admin Authentication ---
def admin_required(func):
    """Decorator to check for admin session."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Using simple session check as per the simplified code structure
        if session.get('admin_logged_in') is None or not session['admin_logged_in']:
            flash('Please log in to access the admin panel.', 'danger')
            return redirect(url_for('main.admin_login'))
        return func(*args, **kwargs)
    return wrapper
# --- END UTILITY ---

## 1. Online Registration Form for Students
@main.route("/", methods=['GET', 'POST'])
@main.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        
        # FIX: Check for unique email inside the app context (routes.py)
        if Applicant.query.filter_by(email=form.email.data).first():
            flash('That email is already registered. Please use a different one.', 'danger')
            # Do not proceed with registration, just return to the form
            return render_template('student/register.html', title='Student Registration', form=form)

        # Proceed with registration
        status_token = secrets.token_hex(16)
        
        applicant = Applicant(
            full_name=form.full_name.data,
            email=form.email.data,
            phone_number=form.phone_number.data,
            program=form.program.data,
            status_token=status_token
        )
        db.session.add(applicant)
        db.session.commit()
        
        # Send initial confirmation email/SMS
        subject = "Admission Application Received"
        body = f"Dear {applicant.full_name}, your application has been received. Your status token is: {status_token}"
        send_email_notification(applicant.email, subject, body)
        
        flash(f'Registration successful! Your application is pending review.', 'success')
        return redirect(url_for('main.register'))
        
    return render_template('student/register.html', title='Student Registration', form=form)

## Status Check (Optional)
@main.route("/status/<token>")
def check_status(token):
    applicant = Applicant.query.filter_by(status_token=token).first_or_404()
    return render_template('student/status.html', applicant=applicant, title="Application Status")

# --- Admin Panel Routes ---

@main.route("/admin/login", methods=['GET', 'POST'])
def admin_login():
    # If already logged in, redirect to dashboard
    if session.get('admin_logged_in'):
        return redirect(url_for('main.admin_dashboard'))

    form = AdminLoginForm()
    if form.validate_on_submit():
        user = AdminUser.query.filter_by(username=form.username.data).first()
        
        # Use proper password checking logic
        if user and user.check_password(form.password.data):
            session['admin_logged_in'] = True # Set session variable
            flash('Logged in successfully.', 'success')
            return redirect(url_for('main.admin_dashboard'))
        else:
            flash('Login Unsuccessful. Check username and password.', 'danger')
            
    return render_template('admin/login.html', title='Admin Login', form=form)
    
@main.route("/admin/logout")
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.admin_login'))


## 2. Admin Approval Panel (Dashboard)
@main.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    # Order by status and then by date
    applicants = Applicant.query.order_by(Applicant.status, Applicant.date_applied.desc()).all()
    return render_template('admin/dashboard.html', title='Admin Dashboard', applicants=applicants)

@main.route("/admin/applicant/<int:applicant_id>", methods=['GET', 'POST'])
@admin_required
def approve_applicant(applicant_id):
    applicant = Applicant.query.get_or_404(applicant_id)
    form = AdminApprovalForm()
    
    if form.validate_on_submit():
        old_status = applicant.status
        new_status = form.status.data
        
        if old_status != new_status:
            applicant.status = new_status
            db.session.commit()
            
            # 3. Email/SMS notification to applicants
            subject = f"Your Admission Status Update: {new_status}"
            body_text = f"Dear {applicant.full_name}, your application for the {applicant.program} program has been updated to: {new_status}.\n\nView status: {url_for('main.check_status', token=applicant.status_token, _external=True)}"
            
            # Send Email
            send_email_notification(applicant.email, subject, body_text)
            
            # Send SMS
            send_sms_notification(applicant.phone_number, f"Status Update: {new_status}. Check email for details.")
            
            flash(f'Status for {applicant.full_name} updated to {new_status} and notification sent.', 'success')
        else:
            flash('Status was not changed.', 'info')
            
        return redirect(url_for('main.admin_dashboard'))
    
    form.status.data = applicant.status # Pre-populate the form
    return render_template('admin/approval.html', title='Review Applicant', applicant=applicant, form=form)