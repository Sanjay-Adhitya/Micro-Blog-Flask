
from email.message import EmailMessage
import ssl
import smtplib

em = EmailMessage()

def send_mail(MAIL_USERNAME, TO_MAIL, subject, body, MAIL_SERVER, PASS_CODE, MAIL_PORT=465):
    try: 
        em['From'] = MAIL_USERNAME
        em['To'] = TO_MAIL
        em['Subject'] = subject
        em.set_content(body)
        ssl_cxt = ssl.create_default_context()
        with smtplib.SMTP_SSL(MAIL_SERVER, MAIL_PORT, context=ssl_cxt) as smpt:
            smpt.login(MAIL_USERNAME, PASS_CODE)
            smpt.sendmail(
                MAIL_USERNAME, TO_MAIL, em.as_string()
        )
        return True
    except:
        return False



# from flask_mail import Message
# from app import mail

# def send_email(subject, sender, recipients, text_body, html_body):
#     msg = Message(subject, sender=sender, recipients=recipients)
#     msg.body = text_body
#     msg.html = html_body
#     mail.send(msg)