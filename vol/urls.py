from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    url(r'^vols', views.index, name='index'),
    path('<int:vol_id>/', views.detail, name='detail'),
    url(r'^somme', views.somme, name='somme'),
    url(r'^add', views.new_vol, name='new_vol'),
    url(r'^immatriculation', views.new_immatriculation, name='new_immatriculation'),
    url(r'^pilote_added_successfully', views.new_pilote_ok, name='new_pilote_ok'),
    url(r'^pilote_add', views.new_pilote, name='new_pilote'),
    url(r'^(?P<pk>[0-9]+)/edit/$', views.edit_vol, name='edit_vol'),
    url(r'^(?P<pk>[0-9]+)/remove/$', views.remove_vol, name='remove_vol'),
    url(r'profile/(?P<username>[a-zA-Z0-9]+)$', views.get_user_profile, name='profile'),
    url(r'^prices', views.prices, name='prices'),
]
