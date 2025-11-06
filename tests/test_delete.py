import unittest
from app import create_app, db
from app.posts.models import Post, PostCategory

class DeletePostTests(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # Create a post to be deleted
        self.post_to_delete = Post(title='Post to Delete', content='...', is_active=True, category='tech')
        db.session.add(self.post_to_delete)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_delete_post_get_page(self):
        """Test: Does the delete confirmation page load (GET)?"""
        response = self.client.get(f'/post/{self.post_to_delete.id}/delete')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Підтвердження видалення'.encode(), response.data)
        self.assertIn(b'Post to Delete', response.data)

    def test_delete_post_submit(self):
        """Test: Is the post deleted after a POST request?"""
        post_id = self.post_to_delete.id
        
        # Check that the post exists before deletion
        post_check = db.session.get(Post, post_id)
        self.assertIsNotNone(post_check)
        
        # Make the POST request to delete
        response = self.client.post(f'/post/{post_id}/delete', follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Пост було видалено.'.encode(), response.data)
        
        # Check we redirected to the main posts page (e.g., 'All Posts' title)
        self.assertIn('Усі пости'.encode(), response.data)
        
        # Check the post is gone from the DB
        deleted_post = db.session.get(Post, post_id)
        self.assertIsNone(deleted_post)