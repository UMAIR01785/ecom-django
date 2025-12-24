from django.contrib import admin
from . models import Account

class AccountAdmin(admin.ModelAdmin):
    list_display=('username','email','is_active','is_superuser')
    filter_horizontal=()
    list_filter=()
    fieldsets=()


admin.site.register(Account,AccountAdmin)
# Register your models here.
