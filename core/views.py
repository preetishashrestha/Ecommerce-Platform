from django.shortcuts import render,get_object_or_404, redirect
from .models import OfferProduct, Category,SubCategory,Product,Brand,Review
from django.db.models import Count, Prefetch, Avg
from django.core.paginator import Paginator
from .forms import ReviewForm


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

    paginator=Paginator(product,1)
    page_n = request.GET.get("page")
    if not page_n or not page_n.isdigit():
        page_n = 1
    data = paginator.get_page(page_n)
    
    # Get page range with ellipsis
    page_range = paginator.get_elided_page_range(number=data.number, on_each_side=1, on_ends=1)
    
    # Convert ellipsis character to '...' string for easier template handling
    page_range_with_dots = ['...' if item == '…' else item for item in page_range]
    
    context = {
        "offer": offer,
        "category": category,
        "product": product,
        "brand": brand,
        "data": data,
        "num": page_range_with_dots,  # Now contains '...' instead of '…'
    }
    return render(request,'core/index.html',context)

def cart(request):
    return render(request,'core/cart.html')

def product_detail(request, id):
    product=get_object_or_404(Product, id=id)
    reviews=product.reviews.all()
    avg_rating=reviews.aggregate(Avg('rating'))["rating__avg"]
    review_count=product.reviews.all().count()

    form=ReviewForm()
    if request.method=='POST':
        form=ReviewForm(data=request.POST)
        if form.is_valid():
            review=form.save(commit=False) # delay
            review.user=request.user
            review.product=product
            review.save()
            return redirect('product_detail',id=product.id)

    context={
        'product':product,
        'form':form,
        'reviews':reviews,
        'range': range(1,6),
        'review_count': review_count,
        'avg_rating':round(avg_rating)
    }
    return render(request,'core/product_detail.html', context)