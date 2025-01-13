import json
import smtplib
import datetime
from email.message import EmailMessage
from flask import  jsonify, request
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime, timedelta, timezone
# Define IST as UTC +5:30
ist = timezone(timedelta(hours=5, minutes=30))

# Get current time in UTC
current_time_utc = datetime.now(timezone.utc)

# Convert UTC to IST
current_time_ist = current_time_utc.astimezone(ist)

# Format current date and time in IST
formatted_time = current_time_ist.strftime("%Y-%m-%d %I:%M:%S %p")

# Email details
smtp_server = "smtp.hostinger.com"
smtp_port = 465  # For SSL
sender_email = "info@swasthyapro.com"  # Your email address
# Receiver's email address
password = "Swasthyapro_info@123#"  # Your email account password (or App Password)
email_contact = "swasthyaprosupport@swathyapro.com"
contact = "9919919910"
def send_email(recieverlist,details):

    # Email subject and body content
    subject = f"SwasthyaPro Appointment Confirmation"
    to_emails = recieverlist  # List of "To" emails Ex. email1,email2,email3
    cc_emails = []  # List of "CC" emails
    all_recipients = to_emails + cc_emails  # Combine both to and cc recipients
    body= details
    # Create the email message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ", ".join(to_emails)  # To field with multiple recipients
    message["Cc"] = ", ".join(cc_emails)  # CC field with multiple recipients
    message["Subject"] = subject

    # Attach the HTML body content
    message.attach(MIMEText(body, "html"))

    # Attach the logo inline in the email body
    image_path = "/content/sample_data/SP SC.png"  # Update this with the actual image path
    try:
        with open(image_path, 'rb') as img_file:
            img = MIMEImage(img_file.read())
            img.add_header('Content-ID', '<clinic_logo>')  # This is the unique identifier for the image
            message.attach(img)
    except FileNotFoundError:
        print(f"Error: The image file at {image_path} was not found.")

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Send the email via SMTP server
    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            server.login(sender_email, password)  # Log in to the server
            server.sendmail(sender_email, all_recipients, message.as_string())  # Send to all recipients (To and CC)
        print("Email sent successfully!")
        return jsonify("Email Sent Successfully!"),200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify("Email Not Sent"),404


def appointmentBody(appointment_id,doctor_department,patient_name,clinic_name,clinic_address,doctor_name,clinic_contact_number,appointment_time):
    has_paid = False
    pay_now_link = "razorpay"
    try:
        body = f"""\
        <html>
        <head>
            <style>
            body {{
                font-family: Arial, sans-serif;
                color: #333;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }}
            .email-container {{
                width: 100%;
                background-color: #ffffff;
                padding: 20px;
                box-sizing: border-box;
            }}
            h1 {{
                color: #28a745; /* Green color */
                text-align: center;
            }}
            p {{
                line-height: 1.6;
            }}
            .table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            .table td {{
                padding: 10px;
                text-align: left;
                border: 1px solid #ddd;
            }}
            .table td:first-child {{
                font-weight: bold;
            }}
            .footer {{
                margin-top: 30px;
                text-align: center;
                font-size: 12px;
                color: #777;
            }}
            .footer a {{
                color: #28a745; /* Green color */
                text-decoration: none;
            }}
            .logo {{
                display: block;
                margin: 0 auto;
                width: 150px;
            }}
            .cta-button {{
                background-color: #28a745; /* Green button */
                color: white;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                border-radius: 5px;
                display: inline-block;
                margin-top: 20px;
            }}
            </style>
        </head>
        <body>
            <div class="email-container">
            <!-- Embedded logo at the top of the email body -->
            <img src="cid:clinic_logo" alt="Clinic Logo" class="logo" />

            <h1>Appointment Confirmation</h1>
            <p>Dear {patient_name},</p>
            <p>Thank you for scheduling your appointment with <strong> {doctor_name}</strong>.</p>
            <p>We are pleased to confirm your appointment. Below are the details:</p>

            <table class="table">
                <tr>
                <td>Your Appointment ID:</td>
                <td>{appointment_id}</td>
                </tr>
                <tr>
                <td>Patient Name:</td>
                <td>{patient_name}</td>
                </tr>
                <tr>
                <td>Doctor's Department:</td>
                <td>{doctor_department}</td>
                </tr>
                <tr>
                <td>Booking Date and Time:</td>
                <td>{formatted_time}</td>
                </tr>
                <tr>
                <td>Appointment Time:</td>
                <td>{appointment_time}</td>
                </tr>
                <tr>
                <td>Location:</td>
                <td{doctor_name}, {clinic_address}</td>
                </tr>
                <tr>
                <td>Doctor/Specialist:</td>
                <td>{doctor_name}</td>
                </tr>
                <tr>
                <td> Clinic Contact Number:</td>
                <td>{clinic_contact_number}</td>
                </tr>
                <tr>
                <td>Contact Email:</td>
                <td>{email_contact}</td>
                </tr>
            </table>

            <p>Please ensure you arrive at least 15 minutes before your scheduled appointment time to complete any necessary paperwork. If you need to reschedule or cancel, kindly notify us at least 2 hours in advance.</p>
            <p>If you have any questions or need further assistance, feel free to contact SwasthyaPro Support Team at {contact}<strong></strong> or reply to this email at <strong>{email_contact}</strong>.</p>

            <p>We look forward to seeing you at your appointment.</p>

            <p>Regards,<br>
            <strong>Team{doctor_name}</strong><br>
            </p>

            <a href="http://www.swasthyapro.com" class="cta-button">Visit Our Website</a>

            <!-- Conditionally show the Pay Now button if not already paid -->
            {"<a href='" + pay_now_link + "' class='cta-button'>Pay Now</a>" if not has_paid else ""}

            <div class="footer">
                <p>For any queries, contact us at <a href="mailto:{email_contact}">{email_contact}</a>.</p>
                <p>&copy; {datetime.now().year} {doctor_name}. All rights reserved.</p>
            </div>
            </div>
        </body>
        </html>
        """
        return body
    except Exception as e:
        print(f"Error in preparing body: {e}")
        return None