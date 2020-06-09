import os
import pathlib
import unittest
from flask import session

from dotenv import load_dotenv
env_dir = pathlib.Path(__file__).parents[1]
load_dotenv(os.path.join(env_dir, '.flaskenv'))

from author.models import Author
from application import db
from application import create_app as create_app_base
from utils.test_db import TestDB

class AuthorTest(unittest.TestCase):
    def create_app(self):
        return create_app_base(
            SQLALCHEMY_DATABASE_URI=self.db_uri,
            DEBUG=True,
            WTF_CSRF_ENABLED=False,
            SECRET_KEY='mySecret'
        )

    def setUp(self):
        self.test_db = TestDB()
        self.db_uri = self.test_db.create_db()
        self.app_factory = self.create_app()
        self.app = self.app_factory.test_client()
        with self.app_factory.app_context():
            db.create_all()

    def tearDown(self):
        with self.app_factory.app_context():
            db.drop_all()
        self.test_db.drop_db()

    def user_dict(self):
        return dict(
            full_name='John Smith',
            email='jsmith@example.com',
            password='test1234', # AssertionError is raised if password is not >= 8
            confirm='test1234'
        )

    def test_user_register(self):
        rv = self.app.post('/register', data=self.user_dict(),
            follow_redirects=True)
        # import pdb; pdb.set_trace()
        assert 'You are registered' in str(rv.data)

        with self.app as c:
            rv = c.get('/')
            assert Author.query.filter_by(email=self.user_dict()['email']).count() == 1

        rv = self.app.post('/register', data=self.user_dict(),
            follow_redirects=True)
        assert 'Email already in use' in str(rv.data)

        user2 = self.user_dict()
        user2['email'] = 'john@example.com'
        user2['confirm'] = 'test4567'

        rv = self.app.post('/register', data=user2,
            follow_redirects=True)
        assert 'Passwords must match' in str(rv.data)

    def test_user_login(self):
        rv = self.app.post('/register', data=self.user_dict())

        with self.app as c:
            rv = c.post('/login', data=self.user_dict(),
                follow_redirects=True)
            assert session['id'] == 1

        with self.app as c:
            rv = c.get('/logout', follow_redirects=True)
            assert session.get('id') is None

        user2 = self.user_dict()
        user2['password'] = 'test4567'
        rv = self.app.post('/login', data=user2, 
            follow_redirects=True)
        assert 'Incorrect email or password' in str(rv.data)

        user3 = self.user_dict()
        user3['email'] = 'noone@example.com'
        rv = self.app.post('/login', data=user3,
            follow_redirects=True)
        assert 'Incorrect email or password' in str(rv.data)
    