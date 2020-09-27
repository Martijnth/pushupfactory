from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from main.models import Users


# Register out own model admin, based on the default UserAdmin
@admin.register(Users)
class CustomUserAdmin(UserAdmin):
    pass
