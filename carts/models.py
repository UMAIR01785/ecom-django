from django.db import models
from ecom_app.models import Category_item
# Create your models here.


class Cart(models.Model):
    cart_id=models.CharField( max_length=50)
    date_added=models.DateTimeField( auto_now_add=True)
    
    
    def __str__(self):
        return self.cart_id
    
    
class CartItem(models.Model):
    item=models.ForeignKey(Category_item, on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    is_active=models.BooleanField(default=True)
    
    
    @property
    def sub_total(self):
        return self.item.price* self.quantity
        
    
    def __str__(self):
        return self.item