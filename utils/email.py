import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


class Email():
    def __init__(self,userobject,smtp_host,smtp_port,smtp_user,smtp_password,smtp_sender_email):
        self.user = userobject
        self.smtp_host= smtp_host
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.smtp_sender_email = smtp_sender_email

    def send_email(self):
        msg = MIMEMultipart()
        msg['From'] = self.smtp_sender_email
        msg['To'] = self.user.email
        msg['Subject'] = 'Notification of Account Creation'
        message = self.generate_email_template()
        msg.attach(MIMEText(message,'html'))
        fp = open('images/logo.png', 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        pf = open('images/data-privacy.png','rb')
        msgI = MIMEImage(pf.read())
        pf.close()
        msgImage.add_header('Content-ID', '<image1>')
        msgI.add_header('Content-ID','<image2>')
        msg.attach(msgImage)
        msg.attach(msgI)
        try:
           smtpObj = smtplib.SMTP(self.smtp_host,port=self.smtp_port)
           smtpObj.starttls()
           smtpObj.login(self.smtp_user,self.smtp_password)
           smtpObj.sendmail(self.smtp_sender_email, [self.user.email],msg=msg.as_string())
           smtpObj.quit()
           print("Successfully sent email to %s" %(self.user.email))
           return True
        except Exception as e:
           print("Error: unable to send email")
           print(e)
           return False
    
    def generate_email_template(self):
        with open('emailTemplate/inviteUserTemplate.html','r') as f:
            message = f.read()
            message = message.replace('LDAPUSER',self.user.uid)
            message = message.replace('LDAPPASSWORD',self.user.password)
            return message