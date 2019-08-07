""" Create your models here. """
from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
import cloudinary
from cloudinary.models import CloudinaryField
from django.contrib.contenttypes.fields import GenericRelation

from hitcount.models import HitCount, HitCountMixin


class Color(models.Model):
    color_id = models.AutoField(primary_key=True)
    color_name = models.CharField(max_length=20)

    def __str__(self):
        return self.color_name


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    sub_category_id = models.AutoField(primary_key=True)
    category_id = models.ForeignKey(Category, related_name='sub_categories', on_delete=models.CASCADE)
    sub_category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.sub_category_name


class ClothType(models.Model):
    cloth_type_id = models.AutoField(primary_key=True)
    cloth_type_name = models.CharField(max_length=100)

    def __str__(self):
        return self.cloth_type_name


class ClothSize(models.Model):
    cloth_size_id = models.AutoField(primary_key=True)
    cloth_size_name = models.CharField(max_length=100)

    def __str__(self):
        return self.cloth_size_name


class ShirtSleeves(models.Model):
    shirt_sleeves_id = models.AutoField(primary_key=True)
    shirt_sleeves_Type = models.CharField(max_length=50)

    def __str__(self):
        return self.shirt_sleeves_Type


class ClothPrint(models.Model):
    cloth_Print_id = models.AutoField(primary_key=True)
    cloth_Print_Name = models.CharField(max_length=50)

    def __str__(self):
        return self.cloth_Print_Name


class ClothFitting(models.Model):
    cloth_fitting_id = models.AutoField(primary_key=True)
    cloth_fitting_Name = models.CharField(max_length=50)

    def __str__(self):
        return self.cloth_fitting_Name


class CollarType(models.Model):
    collar_type_id = models.AutoField(primary_key=True)
    collar_type_name = models.CharField(max_length=50)

    def __str__(self):
        return self.collar_type_name


class MaterialType(models.Model):
    material_type_id = models.AutoField(primary_key=True)
    material_type_name = models.CharField(max_length=50)

    def __str__(self):
        return self.material_type_name


class Product(models.Model, HitCountMixin):
    product_id = models.AutoField(primary_key=True)
    product_sku_no = models.CharField(max_length=50)
    product_title = models.CharField(max_length=200)
    product_unit_price = models.FloatField()
    product_selling_price = models.FloatField()
    product_description = models.CharField(max_length=500)
    product_sub_category_id = models.ForeignKey(SubCategory, related_name='products', on_delete=models.CASCADE)
    product_clothes_type_id = models.ForeignKey(ClothType, related_name='products', on_delete=models.CASCADE)
    product_clothes_print_id = models.ForeignKey(ClothPrint, related_name='products', on_delete=models.CASCADE)
    product_shirt_sleeve_id = models.ForeignKey(ShirtSleeves, related_name='products', on_delete=models.CASCADE)
    product_color = models.ManyToManyField(Color, blank=True, related_name='products')
    product_size = models.ManyToManyField(ClothSize, blank=True, related_name='products')
    product_fitting = models.ManyToManyField(ClothFitting, blank=True, related_name='products')
    product_collar_type_id = models.ForeignKey(CollarType, related_name='products', on_delete=models.CASCADE)
    product_material_type_id = models.ForeignKey(MaterialType, related_name='products', on_delete=models.CASCADE)
    date = models.DateTimeField('Date')
    product_average_rating = models.FloatField(default=0)
    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation')

    def get_colors(self):
        return "\n".join([c.color_name for c in self.product_color.all()])

    def get_sizes(self):
        return "\n".join([s.cloth_size_name for s in self.product_size.all()])

    def get_fittings(self):
        return "\n".join([f.cloth_fitting_Name for f in self.product_fitting.all()])

    def __str__(self):
        return ("{}-{}-{}".format(self.product_id, self.product_sku_no, self.product_title))
        # return f"{self.product_id}-{self.product_sku_no}-{self.product_title}"


class ProductImage(models.Model):
    product_image_id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Product, related_name='products', on_delete=models.CASCADE)
    # product_image = models.ImageField(upload_to = 'products_images', default = 'pic_folder/None/no-img.jpg')
    product_image = cloudinary.models.CloudinaryField('image')

    def image_tag(self):
        if self.product_image:
            return mark_safe('<img src="%s" style="width: 45px; height:45px;" />' % self.product_image.url)
        else:
            return 'No Image Found'

    image_tag.short_description = 'Image'



class CustomerProductReview(models.Model):

    product_review_text = models.CharField(max_length=250)
    product_id = models.ForeignKey(Product, related_name='customer_product_reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='customer_product_reviews', on_delete=models.CASCADE)
    date = models.DateTimeField('Date')


class ProductRating(models.Model):
    product_rating_id = models.CharField(primary_key=True, max_length=1)
    product_rating_text = models.CharField(max_length=25)

    def __str__(self):
        return self.product_rating_id


class CustomerProductRating(models.Model):
    class Meta:
        unique_together = (('product_id', 'user'),)

    product_rating_id = models.ForeignKey(ProductRating, related_name='customer_product_ratings',
                                          on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, related_name='customer_product_ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='customer_product_ratings', on_delete=models.CASCADE)
