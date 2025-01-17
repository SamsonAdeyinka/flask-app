import unittest

from flask import abort, url_for
from flask_testing import TestCase
from os import getenv
from application import app, db
from application.models import User


class TestBase(TestCase):

    def create_app(self):

        # pass in test configurations
        # config_name = 'testing'
       #  app.config.update(SQLALCHEMY_DATABASE_URI='mysql+pymysql://'+str(getenv('MYSQL_USER'))+':'+str(getenv('MYSQL_PASS'))+'@'+str(getenv('MYSQL_URL'))+'/'+str(getenv('MYSQL_DB_TEST'))        )
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@35.246.47.157/test_flaskdb'
        
        
        return app
    def setUp(self):
        """
        Will be called before every test
        """

        db.session.commit()
        db.drop_all()
        db.create_all()

        # create test admin user
        admin = User(email="admin@admin.com", password="admin2016")

        # create test non-admin user
        employee = User(email="test@user.com", password="test2016")

        # save users to database
        db.session.add(admin)
        db.session.add(employee)
        db.session.commit()
        
    def tearDown(self):
        """
        Will be called after every test
        """

        db.session.remove()
        db.drop_all()

class testing(TestBase):
    
    def test_homepage_view(self):
        response = self.client.get(url_for('home'))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        response = self.client.get(url_for('login'))
        self.assertEqual(response.status_code, 200)

    def test_user_view(self):
        target_url = url_for('user', user_id=1)
        redirect_url = url_for('login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirect(response, redirect_url)

