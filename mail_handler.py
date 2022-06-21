import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
class email_handler():
    
    def __init__(self):
        self.status = "created"
    
    def send_register_mail(self, email):
        msg = MIMEMultipart() 
        msg['subject'] = 'CMDIdle Registration Confirmation'
        msg['From'] = ''
        msg['to'] = email
        msg.attach("""\
        Hello {},

        Thank you for joining CMDIdle!

        We’d like to confirm that your account was created successfully.

        If you experience any issues logging into your account, reach out to us on our discord server: https://discord.gg/tKZDSZwAt9

        Best,
        Windows
        """
        )
        
        
        context = ssl.create_default_context()
        return