from django.shortcuts import render,redirect,get_object_or_404
from store.models import Product,Variation
from .models import Cartitem,Carts

def _cart_id(request):
    carts=request.session.session_key
    if not carts:
        carts=request.session.create()
    return carts


def cart_dec(request,product_id):
    cart=Carts.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(Product,id=product_id)
    cart_item=Cartitem.objects.get(cart=cart,product=product)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('carts')

def cart_remove(request,product_id):
    cart=Carts.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(Product,id=product_id)
    cart_item=Cartitem.objects.get(cart=cart,product=product)
    cart_item.delete()
    return redirect('carts')


def add_cart(request,product_id):
    product=Product.objects.get(id=product_id)
    product_variation=[]
    if request.method =="POST":
        for item in request.POST:
            key=item
            value=request.POST[key]
            try:
                variation=Variation.objects.get(product=product,variation_item__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass
    
    try:
        cart=Carts.objects.get(cart_id=_cart_id(request))
    except Carts.DoesNotExist:
        cart=Carts.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()
    try:
        cart_item=Cartitem.objects.create(product=product,quantity=1,cart=cart)
        if len(product_variation)> 0:
            cart_item.variations.clear()
            for item in product_variation:
                cart_item.variations.add(item)

        # cart_item.quantity +=1
        cart_item.save()
    except Cartitem.DoesNotExist:
        cart_item=Cartitem.objects.create(
            product=product,
            cart=cart,
            quantity=1,
             is_active=True,

        )
        if len(product_variation)> 0:
            cart_item.variations.clear()
            for item in product_variation:
                cart_item.variations.add(item)
        cart_item.save()

       
    return redirect('carts')





# Create your views here.
def carts(request,total=0,quantity=0,cart_item=None):
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
    return render (request, 'store/carts.html',context)