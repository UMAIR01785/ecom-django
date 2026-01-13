from django.db import models

# Create your models here.
class Category(models.Model):
    category_name=models.CharField( max_length=50)
    category_photo=models.ImageField(upload_to='media/category', null=True,blank=True)
    category_slug=models.SlugField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name="Categrory"
        verbose_name_plural="Categories"

    def __str__(self):
        return self.category_name
    

class Category_item(models.Model):
    item_name=models.CharField( max_length=50)
    category_name=models.ForeignKey(Category, on_delete=models.CASCADE)
    price=models.CharField( max_length=50)
    image=models.ImageField(upload_to="media/Item")
    description=models.TextField()
    item_slug=models.SlugField()
    created_at=models.DateTimeField( auto_now_add=True)
    updated_at=models.DateTimeField( auto_now=True)
    is_feature=models.BooleanField(default=False)


    def __str__(self):
        return self.item_name