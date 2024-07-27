from django.contrib import admin
from .models import User, Account, Statement


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "contact_number")


admin.site.register(User, UserAdmin)


class AccountAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "account_number", "balance", "account_type")


admin.site.register(Account, AccountAdmin)


class StatementAdmin(admin.ModelAdmin):
    list_display = ("id", "account", "date", "amount", "balance", "statement_type")


admin.site.register(Statement, StatementAdmin)
