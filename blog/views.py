from flask import Blueprint, session

# Create an instance of the blog blueprint
blog_app = Blueprint('blog_app', __name__)

# Create the default route for our app
@blog_app.route('/')
def index():
    if session.get('full_name'):
        return f"Hi { session['full_name'] }"

    return 'Blog Home'