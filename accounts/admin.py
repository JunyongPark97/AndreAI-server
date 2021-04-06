from django.contrib import admin
from django.utils.safestring import mark_safe
from accounts.models import User


class AccountsAdmin(admin.ModelAdmin):
    list_display = ['pk', 'shop_name', 'user_name', 'phone', 'email', 'created_at']


admin.site.register(User, AccountsAdmin)
