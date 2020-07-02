import json
import unittest
from parser_app.app.app import app
from parser_app.app.models import db


class TagPostCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

        self.app = app.test_client()
        db.create_all()

        
    def test_tag_post_valid(self):
        response = self.app.post('/tags/', data=json.dumps({"url": "https://google.com/"}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"id": 1})

    def test_tag_get_valid(self):
        pass

    def tearDown(self):
        db.drop_all()