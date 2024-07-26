from django.contrib import admin
from .models import User, Account, Statement

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'contact_number')
    search_fields = ('first_name', 'last_name', 'contact_number')
admin.site.register(User,UserAdmin)

class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'account_number', 'balance', 'account_type')
    search_fields = ('user__first_name', 'user__last_name', 'account_number')
    list_filter = ('account_type',)
admin.site.register(Account,AccountAdmin)

class StatementAdmin(admin.ModelAdmin):
    list_display = ('id', 'account', 'date', 'amount', 'balance')
    search_fields = ('account__account_number',)
    list_filter = ('date',)

admin.site.register(Statement,StatementAdmin)