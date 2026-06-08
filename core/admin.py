from django.contrib import admin
from .models import *
admin.site.site_title="MyShop Admin"
admin.site.site_header="Django Project"
admin.site.index_title="MyShop"
# Register your models here.

admin.site.register(OfferProduct)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Brand)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=[
        'id','name','image','price','created_at'
    ]
