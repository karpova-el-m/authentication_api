from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    filter_horizontal = []
    ordering = ["email"]
    list_display = [
        "email",
        "username",
        "is_active",
        "is_staff",
        "is_superuser",
    ]
    list_filter = ["is_staff", "is_superuser", "is_active"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (("Personal Info"), {"fields": ("username",)}),
        (
            ("Permissions"),
            {"fields": ("is_active", "is_staff", "is_superuser")},
        ),
        (("Important dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
    search_fields = ["email", "username"]
