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