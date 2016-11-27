from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from accounts.models import User


class UserAdmin(DjangoUserAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'date_joined', 'is_staff', 'data')
    ordering = ('-date_joined',)

admin.site.register(User, UserAdmin)
