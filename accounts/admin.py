from django.contrib import admin
from .models import Accounts
from django.contrib.auth.admin import UserAdmin
class Accountadmin(UserAdmin):
    list_display =('email','username','first_name','last_name','is_admin','is_active')
    list_display_links = ('email', 'username', 'first_name')
    filter_horizontal=()
    list_filter=()
    fieldsets=()



admin.site.register(Accounts,Accountadmin)
# Register your models here.
