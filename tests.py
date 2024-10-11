import os
# Set the database URL environment variable to use SQLite
os.environ['DATABASE_URL'] = 'sqlite://'

from datetime import datetime, timezone, timedelta
import unittest
# Import the app and database from the main app module
from app import app, db
# Import the User and Post models
from app.models import User, Post


class UserModelCase(unittest.TestCase):
    # Set up the test environment before each test
    def setUp(self):
        # Create an app context and push it to the stack
        self.app_context = app.app_context()
        self.app_context.push()
        # Create all database tables
        db.create_all()

    # Tear down the test environment after each test
    def tearDown(self):
        # Remove session and drop all tables
        db.session.remove()
        db.drop_all()
        # Pop the app context
        self.app_context.pop()

    # Test password hashing functionality
    def test_password_hashing(self):
        u = User(username='susan', email='susan@example.com')
        u.set_password('cat')
        # Ensure that the wrong password returns False
        self.assertFalse(u.check_password('dog'))
        # Ensure that the correct password returns True
        self.assertTrue(u.check_password('cat'))

    # Test the avatar generation from an email hash
    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        # Ensure the avatar URL is generated correctly
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))

    # Test the follow functionality
    def test_follow(self):
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        # Add users to the database
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        # Initially, neither user follows the other
        following = db.session.scalars(u1.following.select()).all()
        followers = db.session.scalars(u2.followers.select()).all()
        self.assertEqual(following, [])
        self.assertEqual(followers, [])

        # John follows Susan
        u1.follow(u2)
        db.session.commit()
        # Check that the follow was successful
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.following_count(), 1)
        self.assertEqual(u2.followers_count(), 1)
        u1_following = db.session.scalars(u1.following.select()).all()
        u2_followers = db.session.scalars(u2.followers.select()).all()
        self.assertEqual(u1_following[0].username, 'susan')
        self.assertEqual(u2_followers[0].username, 'john')

        # John unfollows Susan
        u1.unfollow(u2)
        db.session.commit()
        # Ensure the unfollow was successful
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.following_count(), 0)
        self.assertEqual(u2.followers_count(), 0)

    # Test that users can see posts from followed users
    def test_follow_posts(self):
        # Create four users
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        u3 = User(username='mary', email='mary@example.com')
        u4 = User(username='david', email='david@example.com')
        # Add users to the database
        db.session.add_all([u1, u2, u3, u4])

        # Create four posts with different timestamps
        now = datetime.now(timezone.utc)
        p1 = Post(body="post from john", author=u1, timestamp=now + timedelta(seconds=1))
        p2 = Post(body="post from susan", author=u2, timestamp=now + timedelta(seconds=4))
        p3 = Post(body="post from mary", author=u3, timestamp=now + timedelta(seconds=3))
        p4 = Post(body="post from david", author=u4, timestamp=now + timedelta(seconds=2))
        # Add posts to the database
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        # Set up the following relationships
        u1.follow(u2)  # john follows susan
        u1.follow(u4)  # john follows david
        u2.follow(u3)  # susan follows mary
        u3.follow(u4)  # mary follows david
        db.session.commit()

        # Check that each user sees the correct following posts
        f1 = db.session.scalars(u1.following_posts()).all()
        f2 = db.session.scalars(u2.following_posts()).all()
        f3 = db.session.scalars(u3.following_posts()).all()
        f4 = db.session.scalars(u4.following_posts()).all()
        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])


# Run the tests with high verbosity
if __name__ == '__main__':
    unittest.main(verbosity=2)
