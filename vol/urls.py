from django.urls import path, re_path
from django.conf.urls import url
from vol.views import *

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^somme', views.somme, name='somme'),
    re_path('vols', VolList.as_view(), name='flight_list'),
    path('vol_add', VolCreate.as_view(), name='new_vol'),
    re_path(r'^(?P<pk>[0-9]+)/edit/$', VolUpdate.as_view(), name='edit_vol'),
    re_path(r'^(?P<pk>[0-9]+)/remove/$', VolDelete.as_view(), name='remove_vol'),
    re_path(r'^(?P<pk>\d+)/$', VolDetail.as_view(), name='detail'),
    path('immatriculation_add', ImmatriculationCreate.as_view(), name='new_immatriculation'),
    path('immatriculation_add/<int:pk>/', ImmatriculationUpdate.as_view(), name='edit_immatriculation'),
    path('immatriculation_add/<int:pk>/delete', ImmatriculationDelete.as_view(), name='remove_immatriculation'),
    path('pilote_add', PiloteCreate.as_view(), name='new_pilote'),
    path('pilote_add/<int:pk>/', PiloteUpdate.as_view(), name='edit_pilote'),
    path('pilote_add/<int:pk>/delete', PiloteDelete.as_view(), name='remove_pilote'),
    path('iata_add', CodeIataCreate.as_view(), name='new_code_iata'),
    path('iata_add/<int:pk>/', CodeIataUpdate.as_view(), name='edit_code_iata'),
    path('iata_add/<int:pk>/delete', CodeIataDelete.as_view(), name='remove_code_iata'),
    path('type_avion_add', TypeAvionCreate.as_view(), name='new_type_avion'),
    path('type_avion_add/<int:pk>/', TypeAvionUpdate.as_view(), name='edit_type_avion'),
    path('type_avion_add/<int:pk>/delete', TypeAvionDelete.as_view(), name='remove_type_avion'),
    url(r'^profile/(?P<username>[a-zA-Z0-9]+)$', views.get_user_profile, name='profile'),
    url(r'^profile/(?P<username>[a-zA-Z0-9]+)/edit/$', views.update_user_profile, name='edit_profile'),
]
