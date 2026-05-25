from django.db import models
from cloudinary.models import CloudinaryField
from django_ckeditor_5.fields import CKEditor5Field

class OfferProduct(models.Model):
    title=models.CharField(max_length=200)
    desc=models.TextField()
    price=models.DecimalField(max_digits=8,decimal_places=2)
    image=CloudinaryField("images")
    is_available=models.BooleanField(default=True)
    created_at=models.DateField(auto_now=True)

    def __str__(self):
        return self.title

class Category(models.Model):
    title=models.CharField(max_length=50)

    def __str__(self):
        return self.title
    
class SubCategory(models.Model):
    title=models.CharField(max_length=50)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    
class Brand(models.Model):
    name=models.CharField(max_length=200)
    subcategory=models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True)
        
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name=models.CharField(max_length=50)
    category=models.ForeignKey(Category, on_delete=models.CASCADE) 
    subCategory=models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    desc=CKEditor5Field('Text', config_name='extends')
    image=CloudinaryField('images')
    available=models.BooleanField(default=True)
    stock=models.PositiveSmallIntegerField()
    mark_Price=models.DecimalField(max_digits=10,decimal_places=0)
    discount_percent=models.DecimalField(max_digits=4,decimal_places=2)
    price=models.DecimalField(max_digits=10, decimal_places=2,editable=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    brands=models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.name=self.name.capitalize()
        self.price=self.mark_Price*(1-self.discount_percent/100)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name
class ProductImage(models.Model):
    image=CloudinaryField('images')
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")

    def __str__(self):
        return self.product.name
    