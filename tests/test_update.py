import unittest
from datetime import datetime
from app import create_app, db
from app.posts.models import Post, PostCategory

class UpdatePostTests(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # Create a post to be edited
        self.post_to_update = Post(title='Original Title', content='Original content', is_active=True, category='tech')
        db.session.add(self.post_to_update)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_update_post_get_page(self):
        """Test: Does the 'update' page (GET) load with post data?"""
        response = self.client.get(f'/post/{self.post_to_update.id}/update')
        self.assertEqual(response.status_code, 200)
        # Assuming 'Update Post' is the page title/heading
        self.assertIn('Редагування поста'.encode(), response.data)
        # Check that the form is pre-populated
        self.assertIn(b'Original Title', response.data) 

    def test_update_post_submit(self):
        """Test: Is the post updated after a POST request?"""
        
        post_data = {
            'title': 'Updated Title',
            'content': 'Updated content.',
            'posted': self.post_to_update.posted.strftime('%Y-%m-%dT%H:%M'),
            'category': 'publication',
            # 'is_active' is intentionally omitted to pass False (assuming checkbox logic)
        }

        response = self.client.post(
            f'/post/{self.post_to_update.id}/update', 
            data=post_data, 
            follow_redirects=False # Check redirect location
        )
        
        # Should redirect back to the post detail page
        self.assertEqual(response.status_code, 302) 
        expected_redirect_url = f'/post/{self.post_to_update.id}'
        self.assertIn(expected_redirect_url, response.location)
        
        # Verify the changes in the database
        updated_post = db.session.get(Post, self.post_to_update.id)
        
        self.assertEqual(updated_post.title, 'Updated Title')
        self.assertEqual(updated_post.category, PostCategory.publication)
        self.assertEqual(updated_post.is_active, False)