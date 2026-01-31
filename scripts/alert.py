import smtplib, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Alerts:
    def __init__(self):
        self.port = 587
        self.email_server = 'smtp.gmail.com'
        self.emails = os.environ.get('EMAILS').split(',')
        self.sender_email = os.environ.get('SENDER_EMAIL')
        self.sender_pass = os.environ.get('SENDER_PASS')
        
    def send_email(self, header: str, main_text: str):
        msg = MIMEMultipart()
        msg['From'] = 'Personal Alert'
        msg['To'] = ', '.join(self.emails)
        msg['Subject'] = header
        
        msg.attach(MIMEText(main_text, 'plain'))
        
        try:
            server = smtplib.SMTP(self.email_server, self.port, timeout=10)
            server.starttls()
            server.login(self.sender_email, self.sender_pass)
            server.sendmail(self.sender_email, self.emails, msg.as_string())
        finally:
            server.quit()
            



