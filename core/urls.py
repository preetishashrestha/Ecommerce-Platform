from django.urls import path
from .views import *
urlpatterns = [
    path('', index,name="index"),
    path('cart/',cart, name="cart"),
    path('product_detail/',product_detail, name="product")
]
