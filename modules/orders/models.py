from django.db import models
from django.contrib.auth.models import User
from modules.products.models import Product


# Create your models here.

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_date_time = models.DateTimeField('order_date_time')
    delivery_address = models.CharField(max_length=200)
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    subtotal = models.DecimalField(default=0.00, max_digits=20, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=20, decimal_places=2)

    def __str__(self):
        return ("{}-{}".format(self.order_id, self.user))
        # return f"{self.order_id}-{self.user}"


class ProductOrder(models.Model):
    class Meta:
        unique_together = (('product_id', 'order_id'),)

    product_id = models.ForeignKey(Product, related_name='product_orders', on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, related_name='product_orders', on_delete=models.CASCADE)
    product_quantity = models.IntegerField(default=1)
