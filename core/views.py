from django.shortcuts import render
from .models import OfferProduct, Category,Product, SubCategory
from django.db.models import Count, Prefetch

# Create your views here.
def index(request):
    offer=OfferProduct.objects.filter(is_available=True)
    category=Category.objects.annotate(count_sub=Count("subcategory")).prefetch_related(Prefetch('subcategory_set',queryset=\
    SubCategory.objects.annotate(product_count=Count('product'))))
    product=Product.objects.all()
    context={
        "offer":offer,
        "category":category,
        "product":product
    }
    return render(request,'core/index.html',context)

def cart(request):
    return render(request,'core/cart.html')