from django.contrib import admin
from modules.dashboard.views import thirdparty,site_traffic,interactive_chart,page_view
from django.urls import path

urlpatterns = [
    path('',thirdparty,name='dashboard'),
    path('site_traffic/',site_traffic,name ='site_traffic'),
    path('interactive_chart/',interactive_chart,name ='interactive_chart'),
    path('page_view/',page_view,name ='page_view')
]
