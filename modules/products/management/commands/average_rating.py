from django.core.management.base import BaseCommand
from modules.products.models import Product, CustomerProductRating


class Command(BaseCommand):
    help = 'Add average rating'

    def handle(self, *args, **kwargs):
        products = Product.objects.all()

        for p in products:
            rating = CustomerProductRating.objects.filter(product_id=p.product_id)

            count = 1
            result = 0

            for r in rating:
                result = result + int(r.product_rating_id.product_rating_id)
                count = count + 1

            if count == 1:
                pass
            else:
                count = count - 1


            average_rating = round(result / count)
            p.product_average_rating=average_rating
            print(average_rating)
            p.save()
