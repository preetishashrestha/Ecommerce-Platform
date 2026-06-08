from django.contrib import admin
from .models import *
from django.utils.html import format_html

admin.site.site_title="MyShop Admin"
admin.site.site_header="Django Project"
admin.site.index_title="MyShop"
# Register your models here.

admin.site.register(OfferProduct)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Brand)
@admin.register(Product)

class ProductImageAdmin(admin.TabularInline):
    model=ProductImage
    extra=1
    
class ProductAdmin(admin.ModelAdmin):
    list_display=[
        'id','name','image','price','created_at','display_image'
    ]
    #list_display_links=['name']
    list_editable=['name']
    list_filter=['price','category']
    search_fields=['name']
    inlines=[ProductImageAdmin]
    ordering=['name']

    def display_image(self,obj):
        if obj.image:
            return format_html('<img src="{}" height="100px", width="100px">', obj.image.url)
