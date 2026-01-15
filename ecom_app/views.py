from django.shortcuts import render,get_object_or_404
from . models import Category,Category_item
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    category=Category.objects.all()
    item=Category_item.objects.all().filter(is_available=True)

    context={
        'category':category,
        'item':item
    }
    return render(request,'home.html',context)



def store(request,category_slug=None):
    category=Category.objects.all()  # All categories for dropdown menu
    current_category=None  # Selected category
    item=None
    
    if category_slug != None:
        current_category=get_object_or_404(Category,category_slug=category_slug)
        item=Category_item.objects.filter(category_name=current_category,is_available=True)
        item_count=item.count()
    else:
        item=Category_item.objects.filter(is_available=True)
        
    context={
        'category':category,  # For dropdown menu
        'current_category':current_category,  # For page title
        'item':item,
        'item_count':item_count
    }
    return render(request,'store/item_by_category.html',context)



def item_detail(request,category_slug=None,item_slug=None):
    category=Category.objects.all()
    current_category=None
    item=None
    if category_slug != None and item_slug != None:
        current_category=get_object_or_404(Category,category_slug=category_slug)
        item=get_object_or_404(Category_item,item_slug=item_slug)
    else:
        item=Category_item.objects.filter(is_available=True)
    context={
        'current_category':current_category,
        'category':category,
        'item':item
    }
    return render(request,'store/item_detail.html',context)

def product(request):
    category=Category.objects.all()
    item=Category_item.objects.filter(is_available=True)
    item_count=item.count()
    context={
        'category':category,
        'item':item,
        'item_count':item_count
    }
    return render(request,'store/product.html',context)

@login_required(login_url='login')
def dashboard(request):
    return render(request,'store/dashboard.html')


