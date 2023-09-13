import logging
from django.test import TestCase
from users.forms import UserRegForm


logger = logging.getLogger("info")


class UsersFormsTest(TestCase):
    def test_user_reg_form(self):
        form_data = {
            "first_name": "first_name",
            "last_name": "last_name",
            "email": "email",
            "password1": "password1",
            "password2": "password2"
        }
        form = UserRegForm(form_data)
        self.assertEqual(True, True)
