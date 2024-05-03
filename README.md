# hackgroup15_backend



Create User
Endpoint: /api/users/
Method: POST
Description: Creates a new user.
Request Body:
username (string): The username of the new user.
password (string): The password of the new user.
Response:
201 Created on success with the created user object.
400 Bad Request if username or password is missing or invalid.
409 Conflict if the username already exists.
Authenticate User
Endpoint: /api/auth/
Method: POST
Description: Authenticates a user.
Request Body:
username (string): The username of the user.
password (string): The password of the user.
Response:
200 OK on success with the authenticated user object.
400 Bad Request if username or password is missing.
404 Not Found if the user does not exist.
401 Unauthorized if the password is incorrect.
Get User
Endpoint: /api/users/<int:user_id>/
Method: GET
Description: Retrieves user details by ID.
Response:
200 OK on success with the user object.
404 Not Found if the user does not exist.
Blog Routes
Create Blog Post
Endpoint: /api/blog/<int:user_id>/
Method: POST
Description: Creates a new blog post for a user.
Request Body:
title (string): The title of the blog post.
content (string): The content of the blog post.
date (datetime): The date of the blog post (optional, defaults to current datetime).
Response:
201 Created on success with the created blog post object.
400 Bad Request if title or content is missing.
404 Not Found if the user does not exist.
Get Blog Post
Endpoint: /api/blog/<int:post_id>/
Method: GET
Description: Retrieves a blog post by ID.
Response:
200 OK on success with the blog post object.
404 Not Found if the post does not exist.
Delete Blog Post
Endpoint: /api/blog/<int:post_id>/
Method: DELETE
Description: Deletes a blog post by ID.
Response:
200 OK on success with the deleted blog post object.
404 Not Found if the post does not exist.
Comment Routes
Create Comment
Endpoint: /api/blog/comment/<int:post_id>/
Method: POST
Description: Adds a comment to a blog post.
Request Body:
content (string): The content of the comment.
user_id (int): The ID of the user posting the comment.
Response:
201 Created on success with the created comment object.
404 Not Found if the post does not exist.
Get Comments
Endpoint: /api/blog/<int:post_id>/
Method: GET
Description: Retrieves comments for a blog post.
Response:
200 OK on success with an array of comment objects.
404 Not Found if the post does not exist.
Delete Comment
Endpoint: /api/blog/<int:post_id>/
Method: DELETE
Description: Deletes a comment from a blog post.
Request Body:
comment_id (int): The ID of the comment to delete.
Response:
200 OK on success with the deleted comment object.
404 Not Found if the post or comment does not exist.
