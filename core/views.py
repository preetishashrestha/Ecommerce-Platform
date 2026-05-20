from django.shortcuts import render
from .models import OfferProduct, Category,Product

# Create your views here.
def index(request):
    offer=OfferProduct.objects.filter(is_available=True)
    category=Category.objects.all()
    product=Product.objects.all()
    context={
        "offer":offer,
        "category":category,
        "product":product
    }
    return render(request,'core/index.html',context)

def cart(request):
    return render(request,'core/cart.html')