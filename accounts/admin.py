from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import SignupForm
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = SignupForm
    model = User
    list_display = UserAdmin.list_display + ("university_name", )
    fieldsets = ((UserAdmin.fieldsets[0], ) + ((
        _("Personal info"),
        {
            "fields":
            UserAdmin.fieldsets[1][1]["fields"] + (
                "university_name",
                "phone",
                "address1",
                "address2",
                "state",
                "city",
                "zip_code",
                "gender",
            )
        },
    ), ) + (UserAdmin.fieldsets[2], UserAdmin.fieldsets[3]))
    search_fields = UserAdmin.search_fields + (
        "phone",
        "address1",
        "address2",
        "state",
        "city",
        "zip_code",
        "gender",
        "university_name",
    )
    verbose_name_plural = "Profile"

    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff