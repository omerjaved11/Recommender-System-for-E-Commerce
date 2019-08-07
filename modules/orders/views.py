from django.shortcuts import render
from modules.shopping_cart.models import ShoppingCart, ShoppingCartEntry
from modules.products.models import Product,ProductImage,CustomerProductRating,CustomerProductReview,ProductRating
from modules.orders.models import Order,ProductOrder
import datetime
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from modules.e_commerce_auth.views import login_view

# Create your views here.

def show_all_orders(request):
    try:
        orders = Order.objects.filter(user=request.user)
        ctx = {'orders':orders}
        return render(request, 'all_orders.html',ctx)
    except:
        return login_view(request)

def order_detail(request,order_id):
    order_products = ProductOrder.objects.filter(order_id=order_id)
    final_products = []
    for product in order_products:
        rating = 0
        review = ''
        product_image = ProductImage.objects.filter(product_id=product.product_id.product_id)
        product_image = product_image[0].product_image.url
        try:
            rating = CustomerProductRating.objects.get(product_id=product.product_id, user=request.user).product_rating_id_id
            review = CustomerProductReview.objects.get(product_id=product.product_id, user=request.user)
        except:
            pass
        final_products.append({'product':product,'image':product_image,'rating':rating,"review":review})
    ctx = {'order_products':final_products}
    return render(request, 'order_detail.html',ctx)


def checkout(request):
    cart = ShoppingCart.objects.new_or_get(request)
    try:
        entries = ShoppingCartEntry.objects.filter(cart=cart)

        products = []
        total = cart.total
        sub_total = cart.subtotal

        if sub_total < 10000:
            total = total + 200


        for entry in entries:
            products.append([entry.product.product_title, entry.quantity,entry.product.product_selling_price,(entry.quantity*entry.product.product_selling_price)])
        return render(request, "checkout.html", {"products": products, "total": total,"sub_total":sub_total})
    except:
        return render(request,'checkout.html',{})


@login_required
@csrf_exempt
def order(request):
    # try:
        order_obj = Order()
        subtotal = float(request.POST.get('subtotal'))
        order_obj.subtotal = subtotal
        order_obj.delivery_address = request.POST.get('address')
        order_obj.order_date_time = datetime.datetime.now()
        order_obj.user = request.user
        if order_obj.subtotal < float(10000):
            order_obj.total = subtotal + float(200)
        else:
            order_obj.total = subtotal
        order_obj.save()

        cart = ShoppingCart.objects.new_or_get(request)
        items = ShoppingCartEntry.objects.filter(cart=cart)
        for item in items:
            product_order = ProductOrder()
            product_order.product_id=item.product
            product_order.order_id=order_obj
            product_order.product_quantity=item.quantity
            product_order.save()

        cart.delete()
        return HttpResponse(status=201)
    #
    # except:
    #     return HttpResponse(status=404)
@login_required
@csrf_exempt
def addReview(request):

    product_id = request.POST.get('product_id')
    review_id = request.POST.get('review_id')
    review = request.POST.get('review')

    if(review_id == '0'):
        newproductreview = CustomerProductReview()
        newproductreview.product_review_text = review
        product = Product.objects.get(product_id=product_id)
        newproductreview.product_id = product
        newproductreview.user = request.user
        newproductreview.date = datetime.datetime.now()
        newproductreview.save()

    else:
        productreview = CustomerProductReview.objects.get(id=review_id)
        productreview.product_review_text = review
        productreview.save()

    return HttpResponse(status=201)

@login_required
@csrf_exempt
def addRating(request):

    product_id = request.POST.get('product_id')
    rating = request.POST.get('rating')
    old_rating =0
    product = Product.objects.get(product_id=product_id)

    try:
        old_rating = CustomerProductRating.objects.get(product_id=product,user=request.user)
    except:
        pass

    if old_rating:
        old_rating.product_rating_id = ProductRating.objects.get(product_rating_id=rating)
        old_rating.save()
    else:

        productrating = ProductRating.objects.get(product_rating_id=rating)
        newRating = CustomerProductRating(product_id=product,product_rating_id=productrating,user=request.user)
        newRating.save()


    return HttpResponse(status=201)