from app import mail, create_app # Import mail instance and factory function
from flask import current_app, render_template
from flask_mail import Message
# from twilio.rest import Client # Uncomment if using Twilio

def send_email_notification(recipient, subject, body):
    """Sends an email to the applicant."""
    # Use the app factory to get context when calling from outside a request
    app = create_app() 
    with app.app_context():
        msg = Message(subject, 
                      sender=current_app.config['ADMIN_EMAIL'], 
                      recipients=[recipient])
        msg.body = body
        # Optional: msg.html = render_template('notifications/status_update.html', body=body) 
        try:
            mail.send(msg)
            print(f"✅ Email Sent to: {recipient} with subject: {subject}")
            return True
        except Exception as e:
            # IMPORTANT: This will fail if MAIL_USERNAME/PASSWORD is incorrect or TLS is blocked
            print(f"❌ Email failed. Check mail server settings/credentials. Error: {e}")
            return False

def send_sms_notification(recipient_phone, body):
    """Placeholder for SMS notification (requires a service like Twilio)."""
    # In a production app, you would initialize and use the Twilio client here.
    
    # client = Client(current_app.config['SMS_ACCOUNT_SID'], current_app.config['SMS_AUTH_TOKEN'])
    # message = client.messages.create(
    #     to=recipient_phone, 
    #     from_=current_app.config['SMS_FROM_NUMBER'],
    #     body=body)

    print(f"📱 SMS Placeholder: Sending '{body}' to {recipient_phone}")
    return True