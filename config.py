import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    print(os.environ.get('DATABASE_URL'))
    SQLALCHEMY_DATABASE_URI = "mysql://root:root@localhost/miBlog" #or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE =3
    MAIL_SERVER="smtp.googlemail.com"
    MAIL_PORT=587
    MAIL_USE_TLS=1
    MAIL_ADMIN="cellsplant5@gmail.com"
    MAIL_PASSWORD="@1Asdf0p9o8i7uy"
    PASS_CODE = "wpkxgwtoonodfeig"

