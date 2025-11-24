from django.shortcuts import render,get_object_or_404
from store.models import Product
from category.models import Category
from carts.models import Cartitem,Carts
from carts.views import _cart_id
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
# Create your views here.
def store(request,category_slug=None):
    categories=None
    products=None
    if category_slug != None:
        categories= get_object_or_404(Category,slug=category_slug)
        products=Product.objects.filter(category=categories,is_available=True)
        paginator=Paginator(products,3)
        page=request.GET.get('page')
        page_product=paginator.get_page(page)
        product_count=products.count()
    else:
        products= Product.objects.all().filter(is_available=True).order_by('id')
        paginator=Paginator(products,4)
        page=request.GET.get('page')
        page_product=paginator.get_page(page)

        product_count=products.count()
    context={
            'products':page_product,
            'product_count':product_count,
        }
    return render(request,'store/store.html',context)

def product_detail(request,category_slug,product_slug):
    try:
        single_product=Product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart=Cartitem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e
    context={
        'single_product': single_product,
        'in_cart'       : in_cart
    }

    return render(request,'store/product_details.html',context)

def search(request):
     if 'keyword' in request.GET:
         keyword=request.GET['keyword']
         if keyword:
             products=Product.objects.order_by('-joined_date').filter(Q(decription__icontains=keyword) | Q(product_name__icontains=keyword))
         context= {
              'products': products,
         }
                
                 
     return render(request,'store/store.html',context)
@login_required(login_url='login')
def checkout(request,total=0,quantity=0,cart_item=None):
        tax=0
        grand_total=0
        try:
            cart=Carts.objects.get(cart_id=_cart_id(request))
            cart_items=Cartitem.objects.filter(cart=cart , is_active=True)
            for cart_item in cart_items:
                total += cart_item.product.price * cart_item.quantity
                quantity += cart_item.quantity
                tax=(2*total)/100
                grand_total=tax + total
        except:
            cart_items = []
        context={
            'total':total,
            'quantity':quantity,
            'cart_items':cart_items,
            'tax': tax,
            'grand_total': grand_total
        }

        return render(request,'store/checkout.html',context)