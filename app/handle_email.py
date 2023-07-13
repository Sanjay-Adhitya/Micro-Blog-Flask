from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from email.message import EmailMessage
import ssl, os
import smtplib
from app.models import User
em = EmailMessage()

def send_mail(MAIL_USERNAME, TO_MAIL, subject, body, MAIL_SERVER, PASS_CODE, MAIL_PORT=465):
    token = User().get_reset_password_token()
    
    try: 
        if attachment:
            em = MIMEMultipart()
            em['From'] = str(MAIL_USERNAME)
            em['To'] = str(TO_MAIL)
            em['Subject'] = str(subject)
            file = "./app/Sanjay_Adhitya_S.pdf"
            em.attach(MIMEText(body, 'plain'))
            files = [f for f in os.listdir('./app/') if os.path.isfile(f)]
            print(files)
            with open(file, 'rb') as f:
                attachment=MIMEApplication(f.read(), _subtype='pdf')
                attachment.add_header('content-Disposition','attachment',filename=file)
                em.attach(attachment)
            with smtplib.SMTP_SSL(str(MAIL_SERVER), MAIL_PORT, context=ssl_cxt) as smtp:
                smtp.starttls
                smtp.login(str(MAIL_USERNAME), str(PASS_CODE))
                smtp.send_message(em)
            return True
        else:
            em['From'] = str(MAIL_USERNAME)
            em['To'] = str(TO_MAIL)
            em['Subject'] = str(subject)
            em.set_content(body)
            ssl_cxt = ssl.create_default_context()
            with smtplib.SMTP_SSL(str(MAIL_SERVER), MAIL_PORT, context=ssl_cxt) as smpt:
                smpt.login(str(MAIL_USERNAME), str(PASS_CODE))
                smpt.sendmail(
                    MAIL_USERNAME, TO_MAIL, em.as_string()
            )
            return True
    except Exception as e:
        print(e)
        return False

