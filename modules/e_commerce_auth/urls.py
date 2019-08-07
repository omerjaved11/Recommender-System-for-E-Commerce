
from django.conf.urls import url
from modules.e_commerce_auth.views import (logout_user,login_view,register_view,profile)

urlpatterns = [  # pylint: disable=locally-disabled, invalid-name
    # Examples:
    # url(r'^openshift/', include('openshift.foo.urls')),
    url(r'^login/', login_view, name='login'),
    url(r'^register/', register_view, name='register'),
    url(r'^logout/', logout_user, name='logout'),
    url(r'^profile/', profile, name='profile'),
]
