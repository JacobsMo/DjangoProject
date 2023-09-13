import logging
from django.test import TestCase
from djangoproject.settings import ALLOWED_HOSTS
from django.urls import reverse


logger = logging.getLogger("info")


class UsersViewsTest(TestCase):
    def test_reg_page(self):
        response = self.client.get(f"http://{ALLOWED_HOSTS[1]}:8000{reverse('reg_page')}")
        self.assertEqual(response.status_code, 200)
        logger.info("test_reg_page: OK")

    def test_auth_page(self):
        response = self.client.get(f"http://{ALLOWED_HOSTS[1]}:8000{reverse('auth_page')}")
        self.assertEqual(response.status_code, 200)
        logger.info("test_auth_page: OK")
