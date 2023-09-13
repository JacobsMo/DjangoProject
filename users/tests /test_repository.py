import logging
from django.test import TestCase
from users.models import User
from users.repository import UserRepository


logger = logging.getLogger("info")


class UserRepositoryTest(TestCase):
    def test_get_user_by_id(self):
        user = User.objects.create(
            email="email@mail.com",
            password="some_password"
        )
        
        self.assertEqual(type(UserRepository.get_user_by_id(user_id=user.pk)), User)
        self.assertEqual(UserRepository.get_user_by_id(user_id=2), None)

        logger.info("test_get_user_by_id: OK")
