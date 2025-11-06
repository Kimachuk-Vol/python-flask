import unittest
from datetime import datetime
from app import create_app, db
from app.posts.models import Post, PostCategory

class CreatePostTests(unittest.TestCase):
    
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

    def test_create_post_get_page(self):
        """Test: Does the 'create' page load (GET)?"""
        response = self.client.get('/post/create')
        self.assertEqual(response.status_code, 200)
        # Assuming 'Create Post' is the page title or heading
        self.assertIn('творення поста'.encode(), response.data) 

    def test_create_post_anonymous(self):
        """Test: Does a post get created with author 'Anonymous' if nobody is logged in?"""
        response = self.client.post('/post/create', data={
            'title': 'Test Post Anonymous',
            'content': 'Some content here.',
            'posted': datetime.utcnow().strftime('%Y-%m-%dT%H:%M'),
            'category': 'tech',
            'is_active': True
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Пост успішно створено!'.encode(), response.data)
        
        post = Post.query.filter_by(title='Test Post Anonymous').first()
        self.assertIsNotNone(post)
        self.assertEqual(post.author, 'Anonymous')

    def test_create_post_logged_in(self):
        """Test: Does a post get created with author 'testuser' if logged in (session)?"""
        # Simulate user login
        with self.client.session_transaction() as sess:
            sess['username'] = 'testuser'
            
        response = self.client.post('/post/create', data={
            'title': 'Test Post Logged In',
            'content': 'Some content here.',
            'posted': datetime.utcnow().strftime('%Y-%m-%dT%H:%M'),
            'category': 'news',
            'is_active': True
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Пост успішно створено!'.encode(), response.data)
        
        post = Post.query.filter_by(title='Test Post Logged In').first()
        self.assertIsNotNone(post)
        self.assertEqual(post.author, 'testuser')

    def test_create_post_invalid_data(self):
        """Test: Does the user stay on the page if data is invalid (no title)?"""
        response = self.client.post('/post/create', data={
            'title': '', # Invalid data
            'content': 'Some content here.',
            'category': 'tech',
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        # WTForms validation message
        self.assertIn('This field is required'.encode(), response.data)