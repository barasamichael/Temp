import unittest
import flask
from app import create_app, db
from app.models import Role

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_app_exists(self):
        self.assertFalse(flask.current_app is None)


    def test_app_is_testing(self):
        self.assertTrue(flask.current_app.config["TESTING"])

