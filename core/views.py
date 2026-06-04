from django.shortcuts import render,get_object_or_404, redirect
from .models import OfferProduct, Category,SubCategory,Product,Brand,Review
from django.db.models import Count, Prefetch, Avg
from django.core.paginator import Paginator
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
import uuid
import hmac
import hashlib
import base64

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
    
    top_product=Product.objects.annotate(top_rating=Avg("reviews__rating")).order_by("-top_rating")[:3]

    context = {
        "offer": offer,
        "category": category,
        "product": product,
        "brand": brand,
        "data": data,
        "num": page_range_with_dots,  # Now contains '...' instead of '…'
        "top_product": top_product
    }
    return render(request,'core/index.html',context)

def cart(request):
    return render(request,'core/cart.html')

def product_detail(request, id):
    product=get_object_or_404(Product, id=id)
    reviews=product.reviews.all()
    avg_rating = reviews.aggregate(Avg('rating'))["rating__avg"] or 0
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
    related_product=Product.objects.filter(subCategory=product.subCategory).exclude(id=product.id)
    context={
        'product':product,
        'form':form,
        'reviews':reviews,
        'range': range(1,6),
        'review_count': review_count,
        'avg_rating':round(avg_rating) if avg_rating else 0,
        'related_product':related_product
    }
    return render(request,'core/product_detail.html', context)

'''
Django Shopping Cart
'''

@login_required(login_url="log_in")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("index")

@login_required(login_url="log_in")
def cart_add_detail(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart")


@login_required(login_url="log_in")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="log_in")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="log_in")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="log_in")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")

def generate_signature(data, secret):     
    #signed_field_names must be included in the payload   
    signed_fields = data["signed_field_names"].split(",")        
    # Create message string in exact order    
    message = ",".join([f"{field}={data[field]}" for field in signed_fields]) 
    signature = hmac.new(         
        secret.encode("utf-8"),         
        message.encode("utf-8"),         
        hashlib.sha256  
    ).digest()          
    return base64.b64encode(signature).decode("utf-8")

@login_required(login_url="log_in")
def cart_detail(request):
    cart = request.session.get("cart", {})
    amount=0

    for item in cart.values():
        amount+=item["quantity"]*float(item["price"])

    amount=round(amount,2)
    tax_amount=round(amount*0.13,2)
    total_amount=round(amount+tax_amount,2)
    transaction_uuid=str(uuid.uuid4())
    secret_key='8gBm/:&EnhH.1/q'

    data = {
    "amount": amount,
    "tax_amount": tax_amount,
    "total_amount": total_amount,
    "transaction_uuid": transaction_uuid,
    "product_code": "EPAYTEST",
    "product_service_charge": 0,
    "product_delivery_charge": 0,
    "success_url": "http://127.0.0.1:8000/payments/success_url",
    "failure_url": "http://127.0.0.1:8000/payments/failure_url",
    "signed_field_names": "total_amount,transaction_uuid,product_code",
    
    }

    data["signature"]=generate_signature(data=data,secret=secret_key)

    return render(request, 'core/cart.html', data)


    
