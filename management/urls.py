from django.urls import path
from . import views
from management.views import *
from django.contrib.auth.decorators import permission_required

urlpatterns = [
    # path('', views.management_index, name='management_index'),
    path('', IndexView.as_view(), name='management_index'),
    path('website_performance', views.website_performance, name='website_performance'),
    path('customer_management', permission_required('is_staff')(CustomerList.as_view()), name='customer_management'),
    path('user_management', permission_required('is_staff')(UserList.as_view()), name='user_management'),
    path('customer/add', permission_required('is_staff')(CustomerCreate.as_view()), name='customer_create'),
    path('customer/<int:pk>/', permission_required('is_staff')(CustomerUpdate.as_view()), name='customer_update'),
]
