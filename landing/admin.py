from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import AccountCreationForm, AccountChangeForm

from .models import Account

# Register your models here.
class AccountAdmin(BaseUserAdmin):

    form = AccountChangeForm
    add_form = AccountCreationForm

    list_display = ('email','username','is_active','is_staff','is_superuser','is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields':('email','password')}),
        ('Personal info', {'fields': ('username','first_name','last_name','image')}),
        ('Permissions', {'fields': ('is_admin',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields' : ('email','password1', 'password2')
        }),
    ) 
    search_fields = ('email','username')
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(Account, AccountAdmin)
admin.site.unregister(Group)