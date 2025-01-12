import json
import smtplib
import datetime
from email.message import EmailMessage
from flask import  jsonify, request

# Gmail SMTP server configuration

smtp_server = 'smtp.gmail.com'
smtp_port = 587  # Use 465 for SSL or 587 for TLS

today = datetime.date.today()
date_string = today.strftime('%B %d, %Y')
def send_email():
    data = request.get_json() #data contains recipient_email,subject,body
    subject = data['subject']
    body = data['body']
    sender_email = 'rocktheway.2akash@gmail.com'  
    recipient_email = data['recipient']
    password = '*******' 

    # Create an EmailMessage instance
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email


    try:
        # Connect to the Gmail SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Upgrade the connection to secure TLS
            server.login(sender_email, password)  # Authenticate with the server
            server.send_message(msg)
        return jsonify("Email sent successfully!"),201
    except Exception as e:
        return jsonify("Email not sent successfully!"),404
