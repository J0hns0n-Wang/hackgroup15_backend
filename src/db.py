from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


#### Models ####

class User(db.Model):
    """
    Class for User model
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    blogs = db.relationship("Post", cascade="delete")
    comments = db.relationship("Comment", cascade="delete")

    def __init__(self, **kwargs):
        """
        Initialize a User model
        """
        self.username = kwargs.get("username", "")
        self.password = kwargs.get("password", "")

    def serialize(self):
        """
        Serialize the User model
        """
        return {
            "id": self.id,
            "username": self.username,
            "posts": [p.serialize_without_comments() for p in self.blogs],
            "comments": [c.serialize() for c in self.comments]
        }
        
class Post(db.Model):
    """
    Class for blog model
    """
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    comments = db.relationship("Comment", cascade="delete")
    date = db.Column(db.DateTime, nullable=False)

    def __init__(self, **kwargs):
        """
        Initialize a Post model
        """
        self.title = kwargs.get("title", "")
        self.content = kwargs.get("content", "")
        self.user_id = kwargs.get("user_id", 0)
        self.date = kwargs.get("date")

    def serialize(self):
        """
        Serialize the Post model
        """
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "user_id": self.user_id,
            "date": str(self.date),
            "comments": [c.serialize() for c in self.comments]
        }
        
    def serialize_without_comments(self):
        """
        Serialize the Post model without comments
        """
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "user_id": self.user_id,
            # "date": self.date,
        }

class Comment(db.Model):
    """
    Class for blog model
    """
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)

    def __init__(self, **kwargs):
        """
        Initialize the commment model
        """
        self.content = kwargs.get("content", "")
        self.user_id = kwargs.get("user_id", 0)
        self.post_id = kwargs.get("post_id", 0)

    def serialize(self):
        """
        Serialize the Comment model
        """
        return {
            "id": self.id,
            "content": self.content,
        }

