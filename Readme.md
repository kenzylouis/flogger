This is My blog web app with Flask
---

1\. Setup App
---
- create the root folder
- create virtual env
- create requirements.txt
- create .flaskenv
- create settings.py
- create manage.py
- create application.py
- create the blog folder
- create the __init__.py to make it a module
- create the blog/views.py file which is our blueprint

2\. Setup DB
---
- connect to the database
- create the DB
- create the user
- grant privilege to the DB

3\. Setup Author app
---
- create author folder
- create the __init__.py to make it a module
- create the author/views.py
- in application.py, under import blueprints, add the author_app

4\. Setup model for author app
---
- Create the author/models.py. Remember models extends db.Model
- Create the MySQL DB by issuing a Migration
    * Notes: for Migration to works there needs to be a path between the models.py and the application.py. So we do that in the views.py by imporing the model
    - from the terminal, issue a `flask db init` to create the migrations folder
    - then `flask db migrate` to create the DB

5\. Test the model through shell
---
- Open a `flask shell`
```
>>> from author.models import Author
>>> author = Author(full_name='John Smith', email='jsmith@example.com', password='myPassword')
```
- Trying to add the author in the DB `>>> db.session.add(author)` will result in the following error:
    ``` Traceback (most recent call last):
        File "<console>", line 1, in <module>
        NameError: name 'db' is not defined
    ```
- import the 'db' object to interact with the Database
    ```
    >>> from application import db
    >>> db.session.add(author)
    >>> author.id
    >>> db.session.commit()
    >>> author.id
    1
    >>> Author.query.all()
    [<Author: 'John Smith'>]
    >>> db.session.delete(author)
    >>> db.session.commit()
    >>> Author.query.first()
    >>> Author.query.all()
    []
    >>>
    ```

6\. Create Registration Form
---
* Notes: Pain point with forms:
    * Rendering the form on the page
    * Validation of the Data
    * Reloading fields
    * Using the same form for editing

* This process is more streamline wit Flask-WTF 

- Create the `author/forms.py` file
- update the `author/views.py` file 
- create the `templates/author` folder for the templates under the root of directory
- create the `templates/author/register.html` file
    - remember to add `{{ form.hidden_tag }}` for CSRF (Cross-Site Request Forgery)
        - CSRF are Security Features from WTForms and protect you from a known user forms posting to the server by generating a random token every time the form is rendered
- Test by running `flask run`

7\. Validate the form
---
WTForms provide a method validate_on_submit when creating a form object
- Use `validate_on_submit` to create error hints on the form itself
- add `form.validate_on_submit()` after creating the form object
- update the `register.html` to handle the error on the form
- Use Macros, Allows us to create  re-usable HTML code that can work as a function. When we pass parameters something is retutned based on those parameters. 
- As a practice you can prepend a macro template files with an _ ubderscore just to remind yourself they should not be used by themselves
- create `templates/_formhelpers.html` 
    - the `safe` in the `{{ field(**kwargs)|safe }}` tells the macro to not HTML escape the key-word arguments we are passing it, because it is not user intercode we are passing

8\. Add Style to our app
---
- go to [Bootstrap] (https://getbootstrap.com/) and add the style and the javascript scripts in our `base.html` file.

9\. Process the data from the form
---
- Update the `views.py` and add logic to send the data to the database
- Once you submit a new user, use `flask shell` to query the DB
```
>>> from author.models import Author
>>> Author.query.all()
[<Author: 'Kenzy Louis'>]
>>> author = Author.query.first()
>>> author.__dict__
{'_sa_instance_state': <sqlalchemy.orm.state.InstanceState object at 0x10b548240>, 'id': 2, 'password': 'pbkdf2:sha256:150000$zzS1Gw26$d2650a41496821850d76b508a63e66bc3b5c29450d23dec3581594b9bde92ce9', 'full_name': 'Kenzy Louis', 'email': 'klouis@gmail.com'}
>>>
```
- you can also check the database directly by issuing `mysql`
```
mysql -uflogger_user -pflogger_password
mysql> show databases;
mysql> use flogger;
mysql> show tables;
mysql> select * from author;
|----|-------------|------------------|------------------------------------------------------------------------------------------------|
| id | full_name   | email            | password                                                                                       |
|----|-------------|------------------+------------------------------------------------------------------------------------------------|
|  2 | Kenzy Louis | klouis@gmail.com | pbkdf2:sha256:150000$zzS1Gw26$d2650a41496821850d76b508a63e66bc3b5c29450d23dec3581594b9bde92ce9 |
|----|-------------|------------------|------------------------------------------------------------------------------------------------|
1 row in set (0.00 sec)
mysql> \q
Bye
```

10\. Use PDB, the Python DeBugger
---
- in views.py under the if statement to `validate_on_submit` add:
```
import pdb; pdb.set_trace()
```
this will cause our application to halt and the following prompt will appear:
a `->` indicates the next command that will be run, a `n` + `Enter` execute the next line of command
```
> /Users/klouis/projects/flogger/author/views.py(15)register()
-> hashed_password = generate_password_hash(form.password.data)
(Pdb) form.email.data
'klouis@gmail.com'
(Pdb) form.full_name.data
'Kenzy Louis'
(Pdb) n
```

11\. Add custom error validation
---
- Update `forms.py` and add a custom validation to test uniqueness of the email.

12\. Add Login form
---
- Modify the `forms.py` and add a new class Login
- in the `views.py` add a route to the `/login` URL
- add a template in the `templates` folder for the login called `login.html`

*  Add validation to the form:
    *  Add validation for the `Login` class. This does not take any parameters as when we were validating the email because we are validating the whole form. It is a global validator
        * First check if the form pass the normal validation with the `rv` object.
        * when we return `False`, we mark the form as invalidated.

13\. Session for the Author user
---
When login to a website or app, we need to set cookies so that other pages the logged in user loads receive the user's info and prevents him from seeing pages he is not supposed to as well as keep out not logged in user.

- in the views.py import from flask 
    - redirect: to redirect to the blog page
    - session: to manage session
    - url_for to handle urls redirections

- to check if the cookies were pass, update the blog `views.py`, add the session and get the info that was passed from author

14\. Logout an Author user
---
- in the `author/views.py` remove the session information an redirect to the login pages

15\. Improve communication with user: Flask Flash Messages
---
They are special type of notifications allowing users to consume them and automatically desappear after consumption
- Create a Macro to create messages in a nice wrapper
    - create templates/_flashmessages.html
        - the {% with ... %} {% endwith %} block makes the variables messages availabe only within the block
        - if there is any flash messages we loop through them and display them with the help of a boostrap UI
- Use the Macro in the `templates/author/login.html` with an `include` keyword.
- Update the `author/views.py` file, import flash from flask, update register and logout to use `flash`

16\. Add Unit testing for the Author app
---
- Always add unit test for each feature of the app
- Add the `utils/test_db.py` for a test DB
    - Add `utils/__init__.py` so the module can be imported in other files
- Add the test loader `tests.py` in the root of our project 
- Create the `author/tests.py` file to test our Author app
    - Create a class `AuthorTest`
    - create a method `setUp()`
        - to set up the test db,
        - an app factory,
        - a test app from the app factory that use the test db in its app_context
        - this app_context is a app factory of test_client()
    - create a `tearDown()` method
        - `setUp()` and `tearDown()` are always created befor and after each test case respectively and they are mandatory
    - Add a custom method to quickly create a user dictionary
    - Add our first test case. It needs to start with `test_`
    - We can enhance the test.
        - if an author was created, check it in the database. Do that by by setting up a context to simulate the same thing  we do in the views.py
            - we use the home page because we know our DB can be accessed at this point

17.\ Add unit test for login in the Author app
---
The DB was hanged, before I restarted, I got to do the following commands in the DB:
```mysql> show engine innodb status;``` and  ```mysql> SHOW FULL PROCESSLIST;```

```
mysql> SHOW FULL PROCESSLIST;
|-----|-----------------|-----------------|--------------|---------|--------|---------------------------------|-----------------------|
| Id  | User            | Host            | db           | Command | Time   | State                           | Info                  |
|-----|-----------------|-----------------|--------------|---------|--------|---------------------------------|-----------------------|
|   4 | event_scheduler | localhost       | NULL         | Daemon  | 649873 | Waiting on empty queue          | NULL                  |
| 173 | flogger_user    | localhost:59867 | NULL         | Sleep   |    585 |                                 | NULL                  |
| 174 | flogger_user    | localhost:59869 | flogger_test | Sleep   |    585 |                                 | NULL                  |
| 175 | flogger_user    | localhost:59870 | flogger_test | Query   |    585 | Waiting for table metadata lock | DROP TABLE author     |
| 178 | root            | localhost       | flogger_test | Query   |      0 | starting                        | SHOW FULL PROCESSLIST |
|-----|-----------------|-----------------|--------------|---------|--------|---------------------------------|-----------------------|
5 rows in set (0.00 sec)

mysql>
```

18\. Add Nav bar to the app
---
- under templates create `nav.html`
    - we do not have to use bootstrap.
    - the most important thing use a if statement to control:
        - if user is logged in (session is set), display the name and a link to logout
        - else display a link to login
- in the author/login template add a block to include the nav template
- in the author/register template add a block to include the nav template

19\. Add a model for the blog posts
---
- Create a folder under templates called `blog`
- create an `index.html` under `blog`
- update the index function in views.py for the blog app
- create the `blog/models.py` class to handle our blog post model
    - Create the post class method containing:
        - id, tittle, body ...
        - slug for pretty url 
        - Create the init method, it takes an Author object as parameter
        - always use utc in the models for the time
        - use the `db.relationship` feature of the db instance of SQLAlchemy before the __init__. So instead of quering the DB each time we need an author or a category object, we load/attach them in the blog record with `db.relationship`
            - so we can traverse a post.Author object and get for example `post.author.full_name` to get the author's name
            - so you pass the actual `Author` class, not the table name, to the relationship method
            - you also pass a back reference to the `posts` table
            - so we will have on both Author and Category we will have a post property to get a list of posts an author wrote or how many posts a category contains
                - this is the one-to-many relationship
                - to know which model needs to have the relationship definition, always remember which table is the many side. For ex. one author can have many posts, so we put it on the posts model. a post cannot have more than one author (at least in these model)
                - lazy='dynmaic' helps on how we load the related object in memory (in this case it is as needed and not the full object. just the property needed)

    - Create the category class 
        - it has a name
    - Create the `__rep__` for both classes

20\. Add the form for Blog
---
- create a `forms.py` under the blog app folder
- it should contain:
    - A title
    - A text area for the content
    - A dropdown to select from existing category
    - a text field for new category

21\. Add a template for the Blog
---
- create a `post.html` inside `templates/blog`, use the macro helper to render the field that post method from the views.py will pass
- Add a route to our post by creating the `post` method in the `blog/views.py`
- We need to do a DB migration because we created the Post model
    - run the following
    ```
    flask db migrate
    flask db upgrade
    ```

22\. Add Logic to capture blog post into the DB
---
- update the blog views and add logic after `validate_on_submit`
- for new_category:
    - we need to save the category for the post model needs a category.id, but since this is a new category, it does not exists yet and does not have an id
    - we can temporary save the transaction in memory with a `db.session.flush`
    - then save the category
- if no new category just get the one the user selected from the drop down menu
- strip both title and body for any preceding or trailing spaces
- then create the post object and pass it to our db session to commit it to the DB
- generate a url for the blog using a slug
- after running a test:
    - you can check the record from the DB
        - use mysql directly 
        ```
        mysql -u root
        mysql> use flogger
        mysql> select * from post \G
        ```
        - Or you can check the flask shell
        ```
        flask shell
        >>> from blog.models import Post
        >>> Post.query.fist().__dict__
        ```

23\. Add Login Decorator
---
- To Restrict specific routes unless specific conditions are met, use decorator
-  Decorators are software design pattern: it is basically wrapping a function in another function, therefore expanding it without modifying the inner function internal structure
- make the `/post` route available only if an author is logged in
- under `author` app folder create `decorators.py`
    - Import `wraps` to keep the name of the function being decorated
    - import session to easyly check if there is a session
    - import request from flask so that after redirecting users to the login page, they can return to where they were
- modify the `login` method under `author/views.py` to handle user being redirected back and forth
    - verify if there is a next entry (a url) in the session dictionary, if redirect to that url, then pop it out of the dictionary
- modify our `log/views.py` to include our decorator

24\. Work on the blog Articles using Markdown
---
- create a template under `blog` called `article.html`
    - for the body of our post we use a jinja modifier (`...|markdown`) to apply markdown rendering to our blog
- modify `application.py` to import the flask Mardown module and apply it to our app
- Add a route on the blog/views.py for our article method
    -  Also add a redirect to the article under the post method

25\. Add Unittests for Blog
---
- under the blog app add `tests.py`
- alwas create the `SetUp` and `TearDown` methods.
- create test for:
    - posting a blog without login
    - register and login
    - create the post

    Note: had an issue with ```sys.path.append doesn't work with my flask <APP>/tests.py files```

26\. Update the landing (home) page for the blog
---
- update the `nav.html` template file to add a link to create new post
- update `blog/index.html` file under template to loop through all the posts and display them on the home page
- update the views.py for the blog home page, query all live posts, order them, then return it to the template

27\. Add pagination on the blog index page
---
- in the blog app `views.py` define a page variable that reads a page parameters passed to the route if there is None, it will assign 1 to it.
    - this variable will let us know on which page of the result we are on.
- use the `paginate` function in the sqlalchemy query (daisy-chain it to the existing query)
    - the function `paginate` 
        - truncates the results in set of pages
        - takes 3 paramters: the `page` we are currently on, how many results per page we want (`POSTS_PER_PAGE`), display (or not) a 404 error if we are forced to a page that does not have any results -> if set to `False`, we do not really consider it an error.
- update the `blog/index.html` template
    - add links to navigate through the different pages (old and new posts)

28\. Add image upload function to our blog
---
- Update the `forms.py` and add a field for file called image. Import the necessary modules required for this.
- update `blog/post.html` template and add html code to render the image on our blog form
- update the `blog/model.py` and add a field (column) called image (to store the the name of the image)
    - the name of the image is actually a uuid of length 36
- We changed the DB model, we need to do a DB migration
    - `flask db migrate` then `flask db upgrade`
- update the blog `views.py` and add steps to process the image under
    - Add a function to resize the image and do some math not to distort the image when it will be dispayed on the page
- Add the image to the `index.html` and `article.html` templates

29\. Add editing functionality to our blog app
---
- Instead of creating a template edit.html, use conditional in the post.html template for the action we want to perform
- We get the slug of the post we want to edit, so we will pass post context to the template
- update `views.py` and add the `action` variable
    - add a new route for the edit
        - fetch the post from DB
        - use the PostForm class, but pass it a keyword argument `obj=post`, where post is the post we just fetch from the DB
        - validate the form on submit, keep the original title and image, a use `populate_obj(post)` that Flask_WTF gives you to update matching records of the post object
        - verify if image is changed and handle it like before
        - verify if there is a new category and handle it as appropriate
- update the `article.html` template and add an `edit` functionality

30\. Add delete post functionality to our post and test it
---
- We are not deleting the post for real, we just mark it as not live
- update the `views.py`, add a route for delete
    - set the live field to false in the DB
- create the test for the update and delete post in the blog `tests.py` file