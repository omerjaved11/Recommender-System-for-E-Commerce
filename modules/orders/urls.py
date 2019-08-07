from django.conf.urls import url
from modules.orders import views

urlpatterns = [
    url(r'^addReview/', views.addReview, name='addReview'),
    url(r'^addRating/', views.addRating, name='addRating'),
    url(r'^checkout/', views.checkout, name='checkout'),
    url(r'^all/',views.show_all_orders, name="show_all_orders"),
    url(r'^order_detail/(?P<order_id>\d+)/?$',views.order_detail, name="order_detail"),
    url(r'^',  views.order,name="order"),

]
