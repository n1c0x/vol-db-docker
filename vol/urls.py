from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:vol_id>/', views.detail, name='detail'),
    #path('somme/', views.somme, name='somme'),
    url(r'^somme',views.somme),
]
