###############################################################################
# FILENAME: autoemail.py
# PROJECT: EOC Offline Backtesting Tool
# CLIENT: 
# AUTHOR: Matt Hartigan
# DATE CREATED: 31 May 2022
# DESCRIPTION: Utility file tha contains functions used to send email messages
# via python.
###############################################################################
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import config_params


def send_email_with_attachment(subject, body, footer, attachment):

    # Authenticate
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(config_params['sender_email'], config_params['2fapassword'])

    # Build message
    for receiver in config_params['receiver_email_list']:
        message = MIMEMultipart()
        message['From'] = config_params['sender_email']
        message['To'] = receiver
        message['Subject'] = subject
        message.attach(MIMEText(body + footer, 'plain'))
        message.attach(attachment)

        print(receiver)
        text = message.as_string()
        server.sendmail(config_params['sender_email'], receiver, text)
    #     server.sendmail(config_params['sender_email'], receiver, message + config_params['tagline'])

    # Shutdown
    server.quit()
