import decimal
from django.shortcuts import render
from modules.shopping_cart.models import ShoppingCart , ShoppingCartEntry
from modules.products.models import Product
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
# Create your views here.
def cart_home(request):
    entries= ShoppingCartEntry.get_entries(request)
    try:
        total_quantity = sum([entry['quantity'] for entry in entries])
    except:
        total_quantity = 0

    ctx={"entries":ShoppingCartEntry.get_entries(request),'total_quantity':total_quantity}
    return render(request , "cart.html", ctx)

@csrf_exempt
def add_to_cart(request):
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity'))
    print(product_id,quantity)
    product = Product.objects.filter(product_id=product_id).first()
    cart = ShoppingCart.objects.new_or_get(request)
    entry = ShoppingCartEntry.objects.filter(cart=cart, product=product).first()

    if entry:
        if quantity:
            print("quantity")
            print(quantity)
            print(type(quantity))
            if quantity == 1:
                print("enter in if")
                entry.quantity = entry.quantity + 1
            else:
                entry.quantity = quantity
        else:
          entry.quantity =entry.quantity + 1
        entry.save()
        ShoppingCartEntry.cal_totals(cart)
        return HttpResponse(status=201)
    else:
        entry = ShoppingCartEntry()
        entry.product=product
        entry.cart = cart
        entry.quantity = quantity
        entry.save()
        ShoppingCartEntry.cal_totals(cart)
        return HttpResponse(status=201)

    return HttpResponse(status=404)

def increment_quantity(request):
    product_id = request.POST.get('product_id')
    quantity = request.POST.get('quantity')


@csrf_exempt
def remove_item(request):
    try:
        product_id = request.POST.get('product_id')
        cart = ShoppingCart.objects.new_or_get(request)
        product = Product.objects.get(product_id=product_id)
        entry = ShoppingCartEntry.objects.get(cart=cart, product=product)
        total = entry.quantity*entry.product.product_selling_price
        cart.subtotal = cart.subtotal - decimal.Decimal(total)
        cart.total = cart.total - decimal.Decimal(total)
        cart.save()
        entry.delete()
        return HttpResponse(status=201)
    except:
        return HttpResponse(status=404)


def cart_json(request):
    cart = ShoppingCart.objects.new_or_get(request)
    entries= ShoppingCartEntry.filter_entries(cart=cart)

    final_entries=[]

    for entry in entries:
        final_entry={}
        final_entry['productName']= entry['product'].product_title
        final_entry['quantity']=entry['quantity']
        final_entry['price']=entry['product'].product_selling_price
        final_entry['image_url']=entry['image']
        total = entry['quantity']*entry['product'].product_selling_price
        final_entry['cart_total']=total
        print("my name is adeel")
        print(total)
        print(final_entry['cart_total'])
        final_entries.append(final_entry)

    return HttpResponse(json.dumps(final_entries),content_type='application/json')