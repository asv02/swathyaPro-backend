from flask_mail import Mail, Message

def send_email(app, recipient, subject, body):
    if not recipient or not subject or not body:
        return {'error': 'Missing recipient, subject, or body'}, 400

    try:
        mail = Mail(app)  # Use the provided app instance
        msg = Message(subject, sender='rocktheway.2akash@mailtrap.club', recipients=[recipient])
        msg.body = body
        with app.app_context():  # Ensure the context is correct
            mail.send(msg)
        return print('Email sent successfully!')
    except Exception as e:
        return print(f'Failed to send email: {str(e)}')


def send_reset_email(app,email, reset_link):
    try:
        msg = Message(
            "Password Reset Request",
            sender="noreply@yourdomain.com",
            recipients=[email]
        )
        mail = Mail(app)
        msg.body = f"Click the link to reset your password: {reset_link}"
        with app.app_context():
            mail.send(msg)
        return "Email sent"
    except Exception as e:
        return f"Failed to send email: {str(e)}"
