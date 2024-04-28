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
    """
    Endpoint to create a user
    """
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


# user login
@app.route("/api/auth/", methods=["POST"])
def auth_user():
    """
    Endpoint to authenticate a user
    """
    post_body = json.loads(request.data)
    username = post_body.get("username", "")
    password = post_body.get("password", "")
    
    user = User.query.filter_by(username=username).first()
    if user is None:
        return failure_response("User not found!")
    
    if bcrypt.checkpw(password.encode('utf-8'), user.password):
        return success_response(user.serialize())
    return failure_response("Incorrect password!")


@app.route("/api/users/<int:user_id>/", methods=["GET"])
def get_user(user_id):
    """
    Endpoint to get a user
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found!")
    return success_response(user.serialize())


####### Blog Routes #######

@app.route("/api/blog/<int:user_id>/", methods=["POST"])
def create_blog(user_id):
    """
    Endpoint to create a blog
    """
    post_body = json.loads(request.data)
    title = post_body.get("title", "")
    content = post_body.get("content", "")
    date = post_body.get("date", datetime.datetime.now())
    
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found!")
    
    post = Post(title=title, content=content, user_id=user_id, date = date)
    db.session.add(post)
    db.session.commit()
    return success_response(post.serialize(), 201)


@app.route("/api/blog/<int:post_id>/", methods=["GET"])
def get_blog(post_id):
    """
    Endpoint to get a blog
    """
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        return failure_response("Post not found!")
    return success_response(post.serialize())

@app.route("/api/blog/<int:post_id>/", methods=["DELETE"])
def delete_blog(post_id):
    """
    Endpoint to delete a blog
    """
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        return failure_response("Post not found!")
    
    db.session.delete(post)
    db.session.commit()
    return success_response(post.serialize())


###### Comment Routes #######

@app.route("/api/blog/comment/<int:post_id>/", methods=["POST"])
def create_comment(post_id):
    """
    Endpoint to create a comment
    """
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        return failure_response("Post not found!")
    
    post_body = json.loads(request.data)
    content = post_body.get("content", "")
    user_id = post_body.get("user_id", "")
    
    comment = Comment(content=content, user_id=user_id, post_id=post_id)
    db.session.add(comment)
    db.session.commit()
    return success_response(comment.serialize(), 201)

@app.route("/api/blog/<int:post_id>/", methods=["GET"])
def get_comment(post_id):
    """
    Endpoint to get comments
    """
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        return failure_response("Post not found!")
    return success_response([c.serialize() for c in post.comments])

@app.route("/api/blog/<int:post_id>/", methods=["DELETE"])
def delete_comment(post_id):
    """
    Endpoint to delete a comment
    """
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        return failure_response("Post not found!")
    
    post_body = json.loads(request.data)
    comment_id = post_body.get("comment_id", "")
    comment = Comment.query.filter_by(id=comment_id).first()
    if comment is None:
        return failure_response("Comment not found!")
    
    db.session.delete(comment)
    db.session.commit()
    return success_response(comment.serialize())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)