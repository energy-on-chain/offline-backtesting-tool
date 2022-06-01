###############################################################################
# FILENAME: main.py
# PROJECT: CVC Offline Backtester
# CLIENT: Chainview Capital
# AUTHOR: Matt Hartigan
# DATE CREATED: 31 May 2022
# DESCRIPTION: This is the main runfile for the Chainview Capital offline back
# testing system. It coordinates the evaluation of the different strategies 
# as well as summarizing and outputting the results.
###############################################################################
import smtplib
from config import config_params


server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(config_params['sender_email'], config_params['2fapassword'])
message = "hey it's rex\n"
for receiver in config_params['receiver_email_list']:
    server.sendmail(config_params['sender_email'], receiver, message + config_params['tagline'])
server.quit()
