from django.conf.urls import url
from modules.products import views
# from modules.products.views import search_product
from django.urls import path

urlpatterns = [  # pylint: disable=locally-disabled, invalid-name
    url(r'^shop/(?P<category_name>\w+)/?$', views.show_products, name='show_products'),
    # url(r'^add_review_rating/?$', views.add_review_rating, name='add_review_rating'),
    url(r'^category/(?P<sub_catgory>\d+)/?$', views.sub_category_products, name='sub_category_products'),
    url(r'^product_details/(?P<product_id>\d+)/?$', views.product_details, name='product_details'),
]
