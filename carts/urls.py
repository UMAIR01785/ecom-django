from django.urls import path
from . views import *
urlpatterns = [
    path('', carts , name='carts'),
    path('cart/<int:product_id>/',add_cart,name='add_cart'),
    path('cart_dec/<int:product_id>/<int:cart_item_id>/',cart_dec,name='cart_dec'),
    path('cart_remove/<int:product_id>/<int:cart_item_id>/',cart_remove,name='cart_remove'),
    

]

