from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ["email", "username", "is_active", "is_staff", "is_superuser"]
    search_fields = ["email", "username"]
    ordering = ["email"]
    filter_horizontal = []
    list_filter = ["is_active", "is_staff", "is_superuser"]
