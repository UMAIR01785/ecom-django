from django.contrib import admin
from . models import Product,Variation

class ProductAdmin(admin.ModelAdmin):
    list_display=('product_name','price','stock','joined_date','category')
    prepopulated_fields={'slug':('product_name',)}
# Register your models here.
class VariationAdmin(admin.ModelAdmin):
    list_display=('product','variation_item','variation_value','is_active')
    list_editable=('is_active',)
    list_filter=('product','variation_item','variation_value',)

admin.site.register(Product,ProductAdmin)
admin.site.register(Variation,VariationAdmin)
