import json
from datetime import datetime

from flask_login import current_user, login_user, logout_user, login_required
from flask import request 

from app import app, db
from app.models import User, Post
from app.handle_email import send_mail

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

@app.route('/')
def index():
    if not current_user.is_authenticated:
        return {"msg":"You are Unauthorized"}
    posts = current_user.followed_posts().all()
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
        return {"msg":"You are Unauthorized","err":"User name or password mismatch"}

    login_user(user_exists, remember=user_data["remember_me_flag"])
    # return redirect('/')
    return {
        "msg":"Welcome  {}".format(user_exists.username)
    }

@app.route('/logout', methods=['POST'])
def logout():
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

@app.route('/explore')
@login_required
def explore():
    if not current_user.is_authenticated:
        return {"msg":"You are Unauthorized"}
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

@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    # get user obj from name
    user = User.query.filter_by(username=username).first()
    if user is None:return {"msg":"invalid Username"}
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
    print(user)
    posts = Post().per_user_posts(user)
    print(posts)
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

@app.route('/reset_password_request/<email>', methods=['GET', 'POST'])
def reset_password_request(email):
    if current_user.is_authenticated:
        return {"msg":"You are Unauthorized"}
    user = User.query.filter_by(email=email).first()
    token = user.get_reset_password_token()
    if user:
        send_mail(  
            app.config['MAIL_ADMIN'], 
            user.email, app.config['PASS_RESET_SUB'], 
            token,
            app.config['MAIL_SERVER'], 
            app.config['PASS_CODE'], 
            MAIL_PORT=app.config['MAIL_PORT']
        )
    return {"msg":"sent a mail to {}".format(str(user.email)),"token":token}

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):

    if current_user.is_authenticated:
        return {"msg":"index"}
    data = request.json
    user = User.verify_reset_password_token(token)
    if not user:
        return {"msg":"You are Unauthorized"}
    
    user.set_password(data["password"])
    db.session.commit()
    return {"msg":"Password Reset Done."}

@app.route('/user/<user_id>/post/<post_id>')
def get_post_with_id(user_id, post_id):

    if not current_user.is_authenticated:
        return {"msg":"You are Unauthorized"}
    
    post = Post.query.filter_by(user_id=user_id, id=post_id).first()
    data = {
        "body":post.body
    }
    return data

@app.route('/user/<user_id>', methods=['POST'])
def create_post(user_id):

    post_data = request.json
    if not current_user.is_authenticated:
        return {"msg":"You are Unauthorized"}
    
    post = Post(
        body=post_data["body"], user_id=user_id
    )
    db.session.add(post)
    db.session.commit()
    return {"msg":"created successfully"}

@app.route('/user/<user_id>/post/<post_id>', methods=['PUT'])
def edit_post(user_id, post_id):

    post_data = request.json
    if not current_user.is_authenticated:
        return {"msg":"You are Unauthorized"}

    current_post =  Post.query.filter_by(user_id=user_id, id=post_id).first()

    current_post.body = post_data["body"]
    db.session.commit()
    return {"msg":"edited successfully"}

@app.route('/recuirter/resume_request', methods=['post'])
def send_resume():
    to_email = request.json["email"]
    resp = send_mail(  
            app.config['MAIL_ADMIN'], 
            to_email, "Sanjay Adhitya's Profile", 
            "Sanjay Adhitya's Profile",
            app.config['MAIL_SERVER'], 
            app.config['PASS_CODE'], 
            MAIL_PORT=app.config['MAIL_PORT'],
            attachment= True
        )
    return {"value":str(resp)}
