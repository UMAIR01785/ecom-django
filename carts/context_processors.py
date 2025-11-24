from carts.models import Cartitem, Carts
from carts.views import _cart_id


def cart_counter(request):
    count=0
    if 'admin' in request.path:
        return {}
    else:
        try:
           
            cart=Carts.objects.get(cart_id=_cart_id(request))
            if request.user.is_authenticated:
                 cart_item=Cartitem.objects.filter(user=request.user)
            else:
                cart_item=Cartitem.objects.filter(cart=cart[:1])

            
            for cart_items in cart_item:
                count+=cart_items.quantity
        except Carts.DoesNotExist:
            count =0

    return{'cart_count': count}