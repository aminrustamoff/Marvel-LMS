from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ("username", "first_name", "last_name", "role", "is_active")
    list_filter = ("role", "is_active")

    fieldsets = BaseUserAdmin.fieldsets + (
        ("Qo'shimcha ma'lumot", {"fields": ("role", "phone_number", "avatar")}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Qo'shimcha ma'lumot", {"fields": ("role", "phone_number", "avatar", "first_name", "last_name")}),
    )


admin.site.register(User, UserAdmin)