from flask import Blueprint, session, render_template

from application import db
from blog.forms import PostForm
from blog.models import Post, Category
from author.models import Author

# Create an instance of the blog blueprint
blog_app = Blueprint('blog_app', __name__)

# Create the default route for our app
@blog_app.route('/')
def index():
    return render_template('blog/index.html')

@blog_app.route('/post', methods=('GET', 'POST'))
def post():
    form = PostForm()

    return render_template('blog/post.html',
        form=form
    )