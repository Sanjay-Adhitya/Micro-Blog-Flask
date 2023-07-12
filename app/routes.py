import json, os
from flask import request #, redirect
from app import app, db
from datetime import datetime

from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post

@app.route('/')
def index():
    posts = current_user.followed_posts().all()
    # page = request.args.get('page', 1, type=int)
    # posts = current_user.followed_posts().paginate(
    #     page=page, per_page=app.config['POSTS_PER_PAGE'], 
    #     error_out=False).items
    return_posts = []
    for post in posts:
        return_posts.append(
            {
                "user_id":post.user_id,
                "body":post.body,
                "user_name":User.query.filter_by(id=post.user_id).first().username
            }
        )
    
    return json.dumps({
        "posts":return_posts,
        "currentUser":str(current_user.username)
    })

@app.route('/login', methods=['GET', 'POST'])
def login():
    user_data = request.json
    user_exists = User.query.filter_by(username=user_data["username"]).first()

    if user_exists is None or not user_exists.check_password(user_data["password"]):
        return {"msg":"Unauthorized"}

    login_user(user_exists, remember=user_data["remember_me_flag"])
    # return redirect('/')
    return {
        "msg":"Welcome  {}".format(user_exists.username)
    }

@app.route('/logout', methods=['POST'])
def logout():
    print(current_user)
    logout_user()
    return {"msg":"logged out"}

@app.route('/signup', methods=['POST'])
def register():
    user_data = request.json
    username, email = user_data["username"], user_data["email"]
    password, c_password = user_data["password"], user_data["c_password"]

    # TODO Valid if user name already exists
    if validate_username(username):
        return {"msg":"Please use a different username."}
    # TODO Valid if user email already exists
    if validate_email(email):
        return {"msg":"Please use a different email."}

    # TODO Valid if user password is valid

    # TODO Valid if user password and confirm password are same

    # TODO Create a user with name and email
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return {"msg":"Signed up {}".format(user.username)}

@app.route('/getusr', methods=['GET'])
def get_all_user():
    a = User.query.all()
    print(a)
    return {}

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

def validate_username(username):
        user = User.query.filter_by(username=username).first()
        if user is not None:
            return True
        return False

def validate_email(email):
        user = User.query.filter_by(email=email).first()
        if user is not None:
            return True
        return False

@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    # get user obj from name
    user = User.query.filter_by(username=username).first()
    if user is None:return {"msg":"invalid"}
    if user == current_user:return {"msg":"You cannot follow yourself!"}
    current_user.follow(user)
    db.session.commit()
    return {"msg":"You are following {} yah!".format(user.username)}

@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return {"msg":"invalid"}
    if user == current_user:
        {"msg":"You cannot Un Follow yourself!"}
    current_user.unfollow(user)
    db.session.commit()
    return {"msg":"You are not following {} anymore :)".format(user.username)}

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.followed_posts().all()
    return_posts = []
    for post in posts:
        return_posts.append(
            {
                "user_id":post.user_id,
                "body":post.body,
                "user_name":User.query.filter_by(id=post.user_id).first().username
            }
        )
    
    return json.dumps({
        "posts":return_posts,
        "currentUser":str(user.username)
    })

@app.route('/explore')
@login_required
def explore():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return_posts =[]
    for post in posts:
        return_posts.append(
            {
                "user_id":post.user_id,
                "body":post.body,
                "user_name":User.query.filter_by(id=post.user_id).first().username
            }
        )
    return json.dumps({
        "posts":return_posts
    })
