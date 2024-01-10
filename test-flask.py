

from app import app
from unittest import TestCase
from models import db, User, Post


print('SQL DATABASE: ', app.config['SQLALCHEMY_DATABASE_URI'])


db.drop_all()
db.create_all()


class UsersTest(TestCase):
    def setUp(self):
        Post.query.delete()
        User.query.delete()
        user1 = User(first_name='Rocky', last_name='Squirrel')
        user2 = User(first_name='Bulwinkle',
                     last_name='Moose', image_url='images\moose.jpg')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        self.id1 = user1.id
        self.id2 = user2.id
        post1 = Post(title='I can fly', content='well sort of...',
                     created_at='2024-3-1 22:00:00', user_id=user1.id)
        post2 = Post(title='Where is Boris?', content='I need to find Boris. I want some borscht.',
                     created_at='2024-3-1 22:10:00', user_id=user1.id)
        db.session.add(post1)
        db.session.add(post2)
        db.session.commit()
        self.post1_id = post1.id
        self.post2_id = post2.id

    def tearDown(self):
        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get('/users/')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Moose', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.id2}/')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Moose', html)

    def test_show_new(self):
        with app.test_client() as client:
            resp = client.get('/users/new/')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Create a User', html)

    def test_show_edit(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.id1}/edit/')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Rocky', html)

    def test_show_post(self):
        with app.test_client() as client:
            resp = client.get(f'/posts/{self.post2_id}/')
#            print('RESP', resp.get_data(as_text=True))
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('borscht', html)

    def test_new_post(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.id1}/posts/new/')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Add Post for', html)

    def test_edit_post(self):
        with app.test_client() as client:
            resp = client.get(f'/posts/{self.post2_id}/edit/')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Edit a Post', html)

    def test_new_tag(self):
        with app.test_client() as client:
            resp = client.get(f'/tags/new/')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Create a Tag', html)
