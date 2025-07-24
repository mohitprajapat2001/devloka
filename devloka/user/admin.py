from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import register
from user.models import User


class UserAdmin(UserAdmin):
    pass