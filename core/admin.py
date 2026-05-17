from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(OfferProduct)
admin.site.register(Category)
admin.site.register(SubCategory)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=[
        'id','name','image','price','created_at'
    ]
