from django.shortcuts import render
from . models import Category,Category_item

# Create your views here.
def home(request):
    category=Category.objects.all()
    item=Category_item.objects.all()

    context={
        'category':category,
        'item':item
    }
    return render(request,'home.html',context)




