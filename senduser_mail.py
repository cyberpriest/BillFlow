import smtplib 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart 
GMAIL_USER = ''
GMAIL_PASSWORD = ''

def send_email(email:str,code:str):

    subject = 'this is your  code to login to your account'
    html = '<html><body><p>Your code is: {0}</p></body></html>'.format(code)



    msg = MIMEMultipart('alternative')
    msg['subject'] = subject
    msg['from'] = GMAIL_USER
    msg['to'] = email
    msg.attach(MIMEText(html, 'html'))

    with smtplib.SMTP_SSL('smtp.gmail.com',465) as server:
        server.login(GMAIL_USER,GMAIL_PASSWORD)
        server.sendmail(GMAIL_USER,email,msg.as_string())



