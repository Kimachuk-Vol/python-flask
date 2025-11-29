import unittest
from app import create_app, db
from app.users.models import User

class AuthTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        db.create_all()
        
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_page_loads(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)

    def test_login_page_loads(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_register_user_success(self):
        user_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'pass123',
            'confirm_password': 'pass123'
        }
        
        response = self.client.post('/register', data=user_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Your account has been created'.encode('utf-8'), response.data)
        
        user = User.query.filter_by(email='new@example.com').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'newuser')
        self.assertNotEqual(user.password, 'pass123')

    def test_register_duplicate_email(self):
        existing_user = User(username='olduser', email='exist@test.com', password='password')
        db.session.add(existing_user)
        db.session.commit()

        response = self.client.post('/register', data={
            'username': 'newuser2',
            'email': 'exist@test.com',
            'password': 'pass123',
            'confirm_password': 'pass123'
        }, follow_redirects=True)

        self.assertIn('Ця електронна пошта вже зареєстрована.'.encode('utf-8'), response.data)

    def test_login_success(self):
        password = 'pass123'
        hashed_pwd = User.hash_password(password)
        user = User(username='loginuser', email='login@test.com', password=hashed_pwd)
        db.session.add(user)
        db.session.commit()

        response = self.client.post('/login', data={
            'username': 'loginuser',
            'password': password
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Login successful'.encode('utf-8'), response.data)

    def test_login_invalid_password(self):
        user = User(username='user2', email='u2@test.com', password=User.hash_password('pass123'))
        db.session.add(user)
        db.session.commit()

        response = self.client.post('/login', data={
            'username': 'user2',
            'password': 'wrong12'
        }, follow_redirects=True)

        self.assertIn("Invalid username or password.".encode('utf-8'), response.data)

    def test_logout(self):
        password = 'pass'
        user = User(username='logoutuser', email='out@test.com', password=User.hash_password(password))
        db.session.add(user)
        db.session.commit()

        self.client.post('/login', data={'username': 'logoutuser', 'password': password}, follow_redirects=True)

        response = self.client.get('/logout', follow_redirects=True)

        self.assertIn('You have been logged out'.encode('utf-8'), response.data)
        self.assertIn(b'Login', response.data)

if __name__ == "__main__":
    unittest.main()
