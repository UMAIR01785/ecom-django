from django.shortcuts import render,redirect,get_object_or_404
from ecom_app.models import Category_item
from . models import Cart,CartItem
# Create your views here.
def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart

def carts(request,total=0,quantity=0,cartitem=None):
    tax=0
    grand_total=0
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cartitem=CartItem.objects.filter(cart=cart,is_active=True)
        for cartitems in cartitem:
            total += (cartitems.item.price* cartitems.quantity)
            quantity += cartitems.quantity
        tax = (10 * total)/100
        grand_total=total +tax
            
    except:
        pass
    context={
        'total':total,
        'quantity':quantity,
        'cartitem':cartitem,
        'tax':tax,
        'grand_total':grand_total,
    }
    return render(request,'store/carts.html',context)



def add_cart(request,item_id):
    
    item=Category_item.objects.get(id=item_id)
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart=Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()
    try:
        cartitem=CartItem.objects.get(item=item,cart=cart)
        cartitem.quantity +=1
        cartitem.save()
    except CartItem.DoesNotExist:
        cartitem=CartItem.objects.create(
            item=item,
            cart=cart,
            quantity=1,
            
        )  
        cartitem.save()
    return redirect('carts')


def remove_cart(request,item_id):
    cart=get_object_or_404(Cart,cart_id=_cart_id(request))
    item=get_object_or_404(Category_item,id=item_id)
    cartitem=get_object_or_404(CartItem,item=item,cart=cart)
    
    if cartitem.quantity > 1:
        cartitem.quantity -= 1
    else:
        cartitem.delete()
    
    cartitem.save()
    return redirect('carts')


def remove_cart_item(request,item_id):
    cart=get_object_or_404(Cart,cart_id=_cart_id(request))
    item=get_object_or_404(Category_item,id=item_id)
    cartitem=CartItem.objects.get(item=item,cart=cart)
    
    cartitem.delete()
    return redirect('carts')
        
        
        
    
             