from django.urls import path
from djangoproject.settings import BASE_API_URL
from .views import MailingAPIView, MailingCreationAPIView


urlpatterns = [
    path(f"{BASE_API_URL}/mailing/<int:mailing_id>/", MailingAPIView.as_view(), name="mailing_api"),
    path(f"{BASE_API_URL}/mailing/creation/", MailingCreationAPIView.as_view(), name="mailing_creation"),
]
