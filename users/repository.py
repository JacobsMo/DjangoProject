import logging
from .models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet


logger = logging.getLogger("debug")


class UserRepository:
    @staticmethod
    def get_user_by_id(user_id: int) -> User or None:
        try:
            return User.objects.get(pk=user_id)
        except ObjectDoesNotExist as e:
            logger.warning(e)

    # need to test
    @staticmethod
    def get_users_without_date_joined_field() -> QuerySet:
        return User.objects.all().values("first_name", "last_name", "email", "is_staff", "is_active")
