from django.urls import path
from .views import UserRegView, UserAuthView, UserLogoutView, AccessFailedView, UserAuthByTokenView


urlpatterns = [
    path("reg/", UserRegView.as_view(), name="reg_page"),
    path("auth/", UserAuthView.as_view(), name="auth_page"),
    path("logout/", UserLogoutView.as_view(), name="logout_page"),
    path("access_failed/", AccessFailedView.as_view(), name="access_failed_page"),
    path("auth_by_token/", UserAuthByTokenView.as_view(), name="auth_by_token_page"),
]
