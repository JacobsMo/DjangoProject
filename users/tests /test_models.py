import logging
from django.test import TestCase
from users.models import User


logger = logging.getLogger("info")


class UsersModelsTest(TestCase):
    def test_user_model(self):
        try:
            User.first_name
            User.last_name
            User.date_joined
            User.password
            User.email
            User.is_active
            User.is_staff
        except AttributeError:
            self.assertEqual(True, False)
        self.assertTrue(True, True)
