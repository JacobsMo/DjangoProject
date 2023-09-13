from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "date_joined", "is_staff", "is_superuser")
    list_display_links = ("id", "email", "date_joined", "is_staff", "is_superuser")
    search_fields = ("test", "email", "date_joined", "is_staff", "is_superuser")


admin.site.register(User, UserAdmin)
