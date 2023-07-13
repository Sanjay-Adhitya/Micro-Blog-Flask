import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    PASS_RESET_SUB= "PAssword Reset Mail"
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    print(os.environ.get('DATABASE_URL'))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = os.environ.get('POSTS_PER_PAGE') or 3
    MAIL_SERVER=os.environ.get('MAIL_SERVER')
    MAIL_PORT= os.environ.get('MAIL_PORT')
    MAIL_USE_TLS=1
    MAIL_ADMIN = os.environ.get('MAIL_PORT')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    PASS_CODE = os.environ.get('PASS_CODE')
    