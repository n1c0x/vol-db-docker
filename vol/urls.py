from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('vols/', views.index, name='index'),
    path('<int:vol_id>/', views.detail, name='detail'),
    url(r'^somme', views.somme, name='somme'),
    url(r'^add', views.new_vol, name='new_vol'),
    url(r'^(?P<pk>[0-9]+)/edit/$', views.edit_vol, name='edit_vol'),
    url(r'^(?P<pk>[0-9]+)/remove/$', views.remove_vol, name='remove_vol'),
    url(r'profile/(?P<username>[a-zA-Z0-9]+)$', views.get_user_profile, name='profile'),
    url(r'^prices', views.prices, name='prices'),
]
