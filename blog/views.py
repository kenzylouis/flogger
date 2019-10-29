from flask import Blueprint

# Create an instance of the blog blueprint
blog_app = Blueprint('blog_app', __name__)

# Create the default route for our app
@blog_app.route('/')
def index():
    return 'Blog Home'