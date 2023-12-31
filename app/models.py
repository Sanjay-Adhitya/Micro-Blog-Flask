from datetime import datetime
from time import time
import jwt

from app import db, login, app

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    # To relate a user as the as a follower and followed as another user. 
    followed = db.relationship('User', secondary=followers,
                                primaryjoin=(followers.c.follower_id == id),
                                secondaryjoin=(followers.c.followed_id == id),
                                backref=db.backref('followers', lazy='dynamic'), 
                                lazy='dynamic')
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    # To follow someone. 
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    # To follow someone. 
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    # To check who you follow.
    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    # To get the Post of all the user you are following.
    def followed_posts(self):
        return Post.query.join(
            followers, (
            followers.c.followed_id == Post.user_id
            )).filter(
                        followers.c.follower_id == self.id
            ).order_by(
                    Post.timestamp.desc()
            )

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
    
    def per_user_posts(self, user):
        return self.query.filter_by(
            user_id=user.id
        ).order_by(
            Post.timestamp.desc()
            )

@login.user_loader
def load_user(id):
    return User.query.get(int(id))