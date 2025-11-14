from django.db import models
from django.urls import reverse
from category.models import Category
# Create your models here.
class Product(models.Model):
    product_name=models.CharField( max_length=50)
    slug=models.SlugField(max_length=200, unique=True)
    price=models.IntegerField()
    decription=models.TextField(max_length=300)
    image=models.ImageField(upload_to='photo/product')
    stock= models.CharField( )
    is_available=models.BooleanField(default=True)
    joined_date=models.DateTimeField( auto_now_add=True)
    modified_date=models.DateTimeField( auto_now=True)
    category= models.ForeignKey(Category, on_delete=models.CASCADE)

    def get_url(self):
        return reverse('product_detail',args=[self.category.slug,self.slug])

    def __str__(self):
        return self.product_name
    
class VariationManger(models.Manager):
    def color(self):
        return super(VariationManger,self).filter(variation_item='color',is_active=True)
    def size(self):
        return super(VariationManger,self).filter(variation_item='size',is_active=True)

    
Category_variation=(
    ('color','color'),
    ('size','size'),
)
class Variation(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_item=models.CharField(choices=Category_variation, max_length=50)
    is_active=models.BooleanField(default=True)
    variation_value=models.CharField( max_length=50)
    objects=VariationManger()


    def __str__(self):
        return self.variation_value
