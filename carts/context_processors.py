from . models import CartItem , Cart
from . views import _cart_id



def counter(request):
    count=0
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cartitem=CartItem.objects.all().filter(cart=cart)
        for cartitems in cartitem:
            count += cartitems.quantity
    except:
        None
    return dict(count=count)
    
    
    
    