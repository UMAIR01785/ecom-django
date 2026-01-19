from django.urls import path
from . views import *


urlpatterns = [
    path('',carts,name='carts'),
    path('add_cart/<int:item_id>/',add_cart,name='add_cart'),
    path('remove_cart/<int:item_id>/',remove_cart,name='remove_cart'),
    path('remove_cart_item/<int:item_id>/',remove_cart_item,name='remove_cart_item')
]
