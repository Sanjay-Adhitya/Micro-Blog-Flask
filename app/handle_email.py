
from email.message import EmailMessage
import ssl
import smtplib
from app.models import User
em = EmailMessage()

def send_mail(MAIL_USERNAME, TO_MAIL, subject, body, MAIL_SERVER, PASS_CODE, MAIL_PORT=465):
    token = User().get_reset_password_token()
    
    try: 
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

