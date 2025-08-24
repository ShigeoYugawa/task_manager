# task_manager/accounts/admin.py

from django.utils.translation import gettext as _
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """管理画面で CustomUser を操作可能にする Admin クラス"""

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = (
        "email",
        "nickname",
        "first_name",
        "last_name",
        "is_admin",
        "can_edit",
        "is_active",
        "is_staff",
    )
    list_filter = ("is_admin", "can_edit", "is_staff", "is_active")
    search_fields = ("email", "nickname", "first_name", "last_name")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "nickname", "first_name", "last_name", "password")}),
        (
            _("Permissions"),
            {"fields": ("is_admin", "can_edit", "is_active", "is_staff", "is_superuser")},
        ),
        (_("Important dates"), {"fields": ("last_login", "email_verified_at")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "nickname",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "is_admin",
                    "can_edit",
                    "is_active",
                ),
            },
        ),
    )

