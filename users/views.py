import logging
from typing import Any

from django.views.generic import CreateView, TemplateView, FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect

from .forms import UserRegForm
from .models import User
from core.views import BaseView


logger = logging.getLogger("debug")


class UserRegView(BaseView, CreateView):
    form_class = UserRegForm
    model = User
    template_name = "users/reg.html"
    success_url = reverse_lazy("auth_page")

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if request.session.keys():
            return HttpResponseRedirect(reverse("access_failed_page"))
        return super().get(request, *args, **kwargs)


class UserAuthView(BaseView, LoginView):
    form_class = AuthenticationForm
    template_name = "users/auth.html"

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if request.session.keys():
            return HttpResponseRedirect(reverse("access_failed_page"))
        return super().get(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse_lazy("root_page")


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("auth_page")

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.session.keys():
            return HttpResponseRedirect(reverse("auth_page"))
        return super().get(request, *args, **kwargs)


class UserAuthByTokenView(BaseView, TemplateView):
    template_name = "users/auth_by_token.html"


class AccessFailedView(BaseView, TemplateView):
    template_name = "users/access_failed.html"
