import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, Message, User, Likes, Follows

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


from app import app

db.create_all()

class UserModelTestCase(TestCase):

    def setUp(self):
        db.drop_all()
        db.create_all()

        self.uid = 94566
        u = User.signup('testing', 'testing@test.com', 'password', None)
        u.id = self.uid
        db.session.commit()

        self.u = User.query.get(self.uid)

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res
    
    def test_message_model(self):

        m - Message(
            text='something'
            user_id=self.uid
        )

        db.session.add(m)
        db.session.commit()

        #Should show 1 message
        self.assertEqual(len(self.u.messages), 1)
        self.assertEqual(self.u.messages[0].text, 'something')

    def test_message_likes(self):
        m1 = Message(
            text='something',
            user_id=self.uid
        )

        m2 = Message(
            text='something else',
            user_id=self.uid
        )

        u = User.signup('anothertest', 'hendrix@cool.com', 'password', None)
        uid = 888
        u.id = uid
        db.session.add_all([m1, m2, u])
        db.session.commit()

        u.likes.append(m1)

        db.session.commit()

        1 = Likes.query.filter(Likes.user_id == uid).all()
        self.assertEqual(len(1), 1)
        self.assertEqual(1[0].message_id, m1.id)