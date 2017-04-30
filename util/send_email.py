from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
import smtplib
import sys

def send_mail(filename, receiver):
    emaillist = receiver
    msg = MIMEMultipart()
    msg['Subject'] = filename
    msg['From'] = 'danielzhaochina@gmail.com'
    msg['Reply-to'] = 'danielzhaochina@gmail.com'
    msg.preamble = 'Multipart massage.\n'
    part = MIMEText("Hi, please find the attached file")
    msg.attach(part)
    part = MIMEApplication(open(filename,"rb").read())
    part.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(part)

    if True:
        server = smtplib.SMTP('smtp.dev.garenanow.com', 465)
        server.sendmail(msg['From'], emaillist , msg.as_string())
        print 'send email success to ' + receiver + ' with: ' + filename
        server.close()
    else:
        print 'send email failed to ' + receiver + ' with: ' + filename

send_mail(sys.argv[1], 'danielzhaochina@gmail.com')
