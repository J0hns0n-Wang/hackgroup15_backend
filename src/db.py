from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


#### Models ####

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    blogs = db.relationship("Post", cascade="delete")
    comments = db.relationship("Comment", cascade="delete")

    def __init__(self, **kwargs):
        self.username = kwargs.get("username", "")
        self.password = kwargs.get("password", "")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "posts": [p.serialize() for p in self.posts],
            "comments": [c.serialize() for c in self.comments]
        }
        
class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    comments = db.relationship("Comment", cascade="delete")

    def __init__(self, **kwargs):
        self.title = kwargs.get("title", "")
        self.content = kwargs.get("content", "")
        self.user_id = kwargs.get("user_id", 0)

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "user_id": self.user_id,
            "comments": [c.serialize() for c in self.comments]
        }

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)

    def __init__(self, **kwargs):
        self.content = kwargs.get("content", "")
        self.user_id = kwargs.get("user_id", 0)
        self.post_id = kwargs.get("post_id", 0)

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
        }

