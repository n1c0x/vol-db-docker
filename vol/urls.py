from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:vol_id>/', views.detail, name='detail'),
    url(r'^somme',views.somme, name='somme'),
    url(r'^add',views.new_vol, name='new_vol'),
    url(r'^(?P<pk>[0-9]+)/edit/$', views.edit_vol, name='edit_vol'),
]
