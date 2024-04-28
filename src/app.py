from db import db
from flask import Flask,request
import json
from db import User, Post, Comment

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
    if username == "" or password == "":
        return failure_response("Invalid username or password")
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return success_response(user.serialize(), 201)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)