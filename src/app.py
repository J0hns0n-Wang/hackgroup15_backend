from db import db
from flask import Flask,request
import json
from db import User, Post, Comment
import bcrypt
import datetime

app = Flask(__name__)
db_filename = "cms.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

# generalized response formats
def success_response(body, code=200):
    return json.dumps(body), code


def failure_response(message, code=404):
    return json.dumps({"error": message}), code


#### User Routes ####
@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route("/api/users/", methods=["POST"])
def create_user():
    post_body = json.loads(request.data)
    username = post_body.get("username", "")
    password = post_body.get("password", "")
    
    # check if user exists already
    user = User.query.filter_by(username=username).first()
    if user is not None:
        return failure_response("Username already exists!")
    
    if username == "" or password == "":
        return failure_response("Invalid username or password")
    
    hased_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user = User(username=username, password=hased_password)
    db.session.add(user)
    db.session.commit()
    return success_response(user.serialize(), 201)

@app.route("/api/users/<int:user_id>/", methods=["GET"])
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found!")
    return success_response(user.serialize())

@app.route("/api/blog/<int:user_id>/", methods=["POST"])
def create_blog(user_id):
    post_body = json.loads(request.data)
    title = post_body.get("title", "")
    content = post_body.get("content", "")
    date = 3
    
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found!")
    
    post = Post(title=title, content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()
    return success_response(post.serialize(), 201)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)