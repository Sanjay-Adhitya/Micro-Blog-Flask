
from email.message import EmailMessage
import ssl
import smtplib

em = EmailMessage()

def send_mail(MAIL_USERNAME, TO_MAIL, subject, body, MAIL_SERVER, PASS_CODE, MAIL_PORT=465):
    try: 
        em['From'] = str(MAIL_USERNAME)
        em['To'] = str(TO_MAIL)
        em['Subject'] = str(subject)
        em.set_content(body)
        ssl_cxt = ssl.create_default_context()
        with smtplib.SMTP_SSL(str(MAIL_SERVER), 465, context=ssl_cxt) as smpt:
            smpt.login(str(MAIL_USERNAME), str(PASS_CODE))
            smpt.sendmail(
                MAIL_USERNAME, TO_MAIL, em.as_string()
        )
        return True
    except Exception as e:
        print(e)
        return False



# from flask_mail import Message
# from app import mail

# def send_email(subject, sender, recipients, text_body, html_body):
#     msg = Message(subject, sender=sender, recipients=recipients)
#     msg.body = text_body
#     msg.html = html_body
#     mail.send(msg)