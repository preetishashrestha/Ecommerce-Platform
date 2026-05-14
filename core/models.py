from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.
class OfferProduct(models.Model):
    title=models.CharField(max_length=200)
    desc=models.TextField()
    price=models.DecimalField(max_digits=8, decimal_places=2)
    image = CloudinaryField('image')
    is_available=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
