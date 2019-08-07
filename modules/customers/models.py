from django.db import models
from django.contrib.auth.models import User
import cloudinary
from django.utils.safestring import mark_safe

from cloudinary.models import CloudinaryField


# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, related_name="customer_user", on_delete=models.CASCADE)
    user_image = cloudinary.models.CloudinaryField('image',blank = True,null = True )
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=15)
    date_of_birth = models.DateTimeField()

    def __str__(self):
        return "{0} {1}".format(self.user.first_name, self.user.last_name)

    def image_tag(self):
        if self.user_image:
            return mark_safe('<img src="%s" style="width: 45px; height:45px;" />' % self.user_image.url)
        else:
            return 'No Image Found'

    image_tag.short_description = 'Image'