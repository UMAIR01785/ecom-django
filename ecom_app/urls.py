from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('store/<slug:category_slug>/',views.store,name='product_by_category'),
    path('store/<slug:category_slug>/<slug:item_slug>/',views.item_detail,name='item_detail'),
    path('store/',views.product,name='store'),
    path('dashboard/',views.dashboard,name='dashboard')
    


]