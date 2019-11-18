from flask import Blueprint, session, render_template

# Create an instance of the blog blueprint
blog_app = Blueprint('blog_app', __name__)

# Create the default route for our app
@blog_app.route('/')
def index():
    return render_template('blog/index.html')