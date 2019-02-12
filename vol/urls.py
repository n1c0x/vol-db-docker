from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    url(r'^vols', views.index, name='index'),
    path('<int:vol_id>/', views.detail, name='detail'),
    url(r'^somme', views.somme, name='somme'),
    url(r'^vol_add', views.new_vol, name='new_vol'),
    url(r'^immatriculation_add', views.new_immatriculation, name='new_immatriculation'),
    url(r'^immatriculation/(?P<pk>[0-9]+)/edit/$', views.edit_immatriculation, name='edit_immatriculation'),
    url(r'^immatriculation/(?P<pk>[0-9]+)/remove/$', views.remove_immatriculation, name='remove_immatriculation'),
    url(r'^pilote_add', views.new_pilote, name='new_pilote'),
    url(r'^pilote/(?P<pk>[0-9]+)/edit/$', views.edit_pilote, name='edit_pilote'),
    url(r'^pilote/(?P<pk>[0-9]+)/remove/$', views.remove_pilote, name='remove_pilote'),
    url(r'^iata_add', views.new_iata, name='new_iata'),
    url(r'^iata/(?P<pk>[0-9]+)/edit/$', views.edit_iata, name='edit_iata'),
    url(r'^iata/(?P<pk>[0-9]+)/remove/$', views.remove_iata, name='remove_iata'),
    url(r'^type_avion_add', views.new_type_avion, name='new_type_avion'),
    url(r'^type_avion/(?P<pk>[0-9]+)/edit/$', views.edit_type_avion, name='edit_type_avion'),
    url(r'^type_avion/(?P<pk>[0-9]+)/remove/$', views.remove_type_avion, name='remove_type_avion'),
    url(r'^(?P<pk>[0-9]+)/edit/$', views.edit_vol, name='edit_vol'),
    url(r'^(?P<pk>[0-9]+)/remove/$', views.remove_vol, name='remove_vol'),
    url(r'profile/(?P<username>[a-zA-Z0-9]+)$', views.get_user_profile, name='profile'),
    url(r'^prices', views.prices, name='prices'),
]
