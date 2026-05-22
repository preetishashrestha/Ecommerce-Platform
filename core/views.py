from django.shortcuts import render
from .models import OfferProduct, Category,SubCategory,Product,Brand
from django.db.models import Count, Prefetch
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    offer=OfferProduct.objects.filter(is_available=True)
    brand = Brand.objects.all()
    category=Category.objects.annotate(count_sub=Count("subcategory")).prefetch_related(Prefetch('subcategory_set',queryset=\
    SubCategory.objects.annotate(product_count=Count('product'))))

    sub_id=request.GET.get('subcategory')
    min=request.GET.get('min')
    max=request.GET.get('max')
    if sub_id and max and min:
        product=Product.objects.filter(subCategory=sub_id,price__range=(min,max))
    elif sub_id:
        product=Product.objects.filter(subCategory=sub_id)
    else:
        product=Product.objects.all()

    paginator=Paginator(product,5)
    page_n=request.GET.get("page")#http://127.0.0.1:8081/
    data=paginator.get_page(page_n)#fetch product
    total=data.paginator.num_pages

    context={
        "offer":offer,
        "category":category,
        "product":product,
        "brand":brand,
        "data":data,
        "num":[i+1 for i in range(total)] #[1,2,3]
    }
    return render(request,'core/index.html',context)

def cart(request):
    return render(request,'core/cart.html')
def product_detail(request):
    return render(request,'core/product_detail.html')