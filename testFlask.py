from unittest import TestCase

from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_test'
app.config['SQLALCHEMY_ECHO'] = True

app.config['TESTING'] = False

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UsersViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample user."""
        Post.query.delete()
        User.query.delete()
        

        user = User(first_name="TestTom", last_name="Smith")
        
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id 

        post = Post(title="TestTitle", content="Testing test testing", user_id=user.id)

        db.session.add(post)
        db.session.commit()

        
        self.post_id = post.id


    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestTom', html)

    def test_show_user_profile(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h3>TestTom Smith</h3>', html)

    def test_add_user(self):
        with app.test_client() as client:
            d = {"first_name": "TestTom2", "last_name": "Jones", "image_url": "https://www.atomix.com.au/media/2017/07/StockPhotoBanner.jpg"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestTom2", html)

    def test_edit_user(self):
        with app.test_client() as client:
            d = {"first_name": "TestTommy", "last_name": "Jones", "image_url": "https://www.atomix.com.au/media/2017/07/StockPhotoBanner.jpg"}
            resp = client.post(f"/users/{self.user_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestTommy", html)

    def test_view_post(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestTitle", html)

    def test_add_post(self):
        with app.test_client() as client:
            d = {"title": "TestPostTest2", "content": "Testing adding a post"}
            resp = client.post(f"/users/{self.user_id}/posts/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestPostTest2", html)

