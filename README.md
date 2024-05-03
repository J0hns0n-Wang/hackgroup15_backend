# hackgroup15_backend

# Flask API Documentation

This documentation outlines the API endpoints and their functionalities for the Flask application.

## User Routes

### Create User

- **Endpoint**: `/api/users/`
- **Method**: `POST`
- **Description**: Creates a new user.

### Authenticate User

- **Endpoint**: `/api/auth/`
- **Method**: `POST`
- **Description**: Authenticates a user.

### Get User

- **Endpoint**: `/api/users/<int:user_id>/`
- **Method**: `GET`
- **Description**: Retrieves user details by ID.

## Blog Routes

### Create Blog Post

- **Endpoint**: `/api/blog/<int:user_id>/`
- **Method**: `POST`
- **Description**: Creates a new blog post for a user.

### Get Blog Post

- **Endpoint**: `/api/blog/<int:post_id>/`
- **Method**: `GET`
- **Description**: Retrieves a blog post by ID.

### Delete Blog Post

- **Endpoint**: `/api/blog/<int:post_id>/`
- **Method**: `DELETE`
- **Description**: Deletes a blog post by ID.

## Comment Routes

### Create Comment

- **Endpoint**: `/api/blog/comment/<int:post_id>/`
- **Method**: `POST`
- **Description**: Adds a comment to a blog post.

### Get Comments

- **Endpoint**: `/api/blog/<int:post_id>/`
- **Method**: `GET`
- **Description**: Retrieves comments for a blog post.

### Delete Comment

- **Endpoint**: `/api/blog/<int:post_id>/`
- **Method**: `DELETE`
- **Description**: Deletes a comment from a blog post.

