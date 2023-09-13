import os
from celery import Celery
from .settings import RABBITMQ_DEFAULT_USER, RABBITMQ_DEFAULT_PASS


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoproject.settings")


app = Celery("djangoproject", broker=f"redis://redis:6379")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
