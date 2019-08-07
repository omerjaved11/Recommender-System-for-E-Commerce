from django.db import models
from django.contrib.auth.models import User
from modules.products.models import Product,ProductImage
# Create your models here.

class ShoppingCartManager(models.Manager):


    def new_or_get(self, request):
        if request.user.is_authenticated:
            user_cart_obj = ShoppingCart.objects.filter(user=request.user).first()
            print(user_cart_obj)
            cart_obj = ''
            if user_cart_obj:
                cart_id = request.session.get('cart_id')
                try:
                    cart_obj_temp = ShoppingCart.objects.get(id=cart_id)
                    entries=ShoppingCartEntry.objects.filter(cart=user_cart_obj)
                    entries_temp=ShoppingCartEntry.objects.filter(cart=cart_obj_temp)
                    if entries_temp:
                        for entry in entries_temp:
                            try:
                                record=entries.get(product=entry.product)
                                record.quantity=record.quantity+entry.quantity
                                record.save()
                            except:
                                entry.cart=user_cart_obj
                                entry.save()

                    cart_obj = user_cart_obj
                except:
                    pass
            else:
                cart_id = request.session.get('cart_id')
                cart_obj = ShoppingCart.objects.filter(id=cart_id).first()
                if cart_obj is None:
                    cart_obj = ShoppingCart.objects.new()
                cart_obj.user=request.user
                cart_obj.save()
        else:
            try:
                cart_obj = ShoppingCart.objects.get(id=request.session['cart_id'])
            except:
                cart_obj = ShoppingCart.objects.new()
                request.session['cart_id'] = cart_obj.id
        return cart_obj


    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)





class ShoppingCart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    subtotal = models.DecimalField(default=0.00, max_digits=20, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=20, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = ShoppingCartManager()

    def __str__(self):
        return str(self.id)

class ShoppingCartEntry(models.Model):
    product = models.ForeignKey(Product,  related_name='shoping_cart_entry' ,on_delete=models.CASCADE)
    cart = models.ForeignKey(ShoppingCart, related_name='shoping_cart_entry', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


    def get_entries(request):
        cart_obj = ShoppingCart.objects.new_or_get(request)
        try:
            entries = ShoppingCartEntry.objects.filter(cart=cart_obj)
            if entries:
                return ShoppingCartEntry.filter_entries(cart_obj)
        except ShoppingCartEntry.MultipleObjectsReturned:
            return ShoppingCartEntry.filter_entries(cart_obj)
        except:
            return {}


    def cal_totals(cart):
        entries=ShoppingCartEntry.objects.filter(cart=cart)
        total=0
        for entry in entries:
            total=total+(entry.quantity*entry.product.product_selling_price)
        cart.subtotal = total
        cart.total= total
        cart.save()

    def filter_entries(cart):
        all_entries = ShoppingCartEntry.objects.filter(cart=cart)
        final_entries = []
        for entry in all_entries:
            image = ProductImage.objects.filter(product_id=entry.product.product_id)
            try:
                image = image[image.count() - 1].product_image.url
            except Exception as exp:
                print(exp)
                pass
            dic = {}
            dic['cart'] = entry.cart
            dic['quantity'] = entry.quantity
            dic['product'] = entry.product
            dic['image'] = image
            final_entries.append(dic)

        return final_entries

    def __str__(self):
        return "This entry contains {} {}".format(self.quantity,self.product)