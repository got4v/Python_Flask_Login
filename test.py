import unittest
from app import app, db, User

class LoginTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.create_all()

        # Create a test user
        self.user = User(username='testuser', password='testpassword')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_valid_login(self):
        response = self.app.post('/login', data=dict(
            username='testuser',
            password='testpassword'
        ), follow_redirects=True)
        self.assertIn(b'Dashboard', response.data)

    def test_invalid_username(self):
        response = self.app.post('/login', data=dict(
            username='invaliduser',
            password='testpassword'
        ), follow_redirects=True)
        self.assertIn(b'Invalid username or password', response.data)

    def test_invalid_password(self):
        response = self.app.post('/login', data=dict(
            username='testuser',
            password='wrongpassword'
        ), follow_redirects=True)
        self.assertIn(b'Invalid username or password', response.data)

    def test_blank_fields(self):
        response = self.app.post('/login', data=dict(
            username='',
            password=''
        ), follow_redirects=True)
        self.assertIn(b'This field is required', response.data)

if __name__ == '__main__':
    unittest.main()
