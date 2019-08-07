from django.conf.urls import url

from .views import (cart_home, add_to_cart, remove_item, cart_json)

urlpatterns = [
    url(r'^$', cart_home, name='cart'),
    url(r'^update/', add_to_cart, name='update'),
    url(r'^remove/', remove_item, name='remove'),
    url(r'^get_cart/', cart_json, name='get_cart'),

]
