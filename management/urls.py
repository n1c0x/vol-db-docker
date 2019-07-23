from django.urls import path
from . import views
from management.views import *

urlpatterns = [
    path('', views.management_index, name='management_index'),
    path('website_performance', views.website_performance, name='website_performance'),
    path('customer_management', CustomerList.as_view(), name='customer_management'),
    path('user_management', UserList.as_view(), name='user_management'),
]
