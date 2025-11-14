from django.db import models
from store.models import Product

# Create your models here.
class Carts(models.Model):
    cart_id=models.CharField( max_length=50)
    date_added=models.DateField( auto_now_add=True)

    def __str__(self):
        return self.cart_id
    
class Cartitem(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    cart= models.ForeignKey(Carts, on_delete=models.CASCADE)
    quantity=models.IntegerField()
    is_active=models.BooleanField()

    def sub_total(self):
        return self.product.price * self.quantity


    def __str__(self):
        return str(self.product)
    