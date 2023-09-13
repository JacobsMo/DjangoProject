from django.contrib import admin
from django.urls import include, path
from djangoproject.yasg import urlpatterns as yasg_urls
from djangoproject.settings import BASE_API_URL


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("users.urls")),
    path("", include("core.urls")),
    path("", include("mailing.urls")),
    path('__debug__/', include('debug_toolbar.urls')),
    path('djoser/', include('djoser.urls')),
    path('djoser/auth/', include('djoser.urls.authtoken')),
]

urlpatterns += yasg_urls
