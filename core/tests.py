from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class TravelUserTestCase(TestCase):
    def setUp(self):
        User.objects.create(email="g@g.fr")
        User.objects.create(email="o@o.fr")

    def test_user_have_friends(self):
        julien = User.objects.get(email="g@g.fr")
        xavier = User.objects.get(email="o@o.fr")
        julien.friends.add(xavier)
        self.assertEqual(julien.get_friends()[0].id, xavier.id)
        # self.assertEqual(julien.get_friends()[1], xavier)
# Create your tests here.
