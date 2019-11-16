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