from django.contrib import admin
from .models import Category,Category_item


class CategoryAdmin(admin.ModelAdmin):
    list_display=('category_name','created_at')
    prepopulated_fields={ "category_slug": ("category_name",)}
    
    
class itemAdmin(admin.ModelAdmin):
    list_display=('item_name','category_name','price','created_at')
    readonly_fields=['item_slug']
    
    

admin.site.register(Category,CategoryAdmin)
admin.site.register(Category_item,itemAdmin)
# Register your models here.
