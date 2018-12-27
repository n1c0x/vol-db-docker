from django.shortcuts import render,get_object_or_404
from django.db.models import Sum
from django.http import HttpResponse

from .models import Vol, Immatriculation, TypeAvion

# Create your views here.

def index(request):
    vols_list = Vol.objects.order_by('-date')[:5]
    context = {
        'vols_list': vols_list
    }
    return render(request, 'vol/index.html', context)

def detail(request,vol_id):
    vol = get_object_or_404(Vol, pk=vol_id)
    return render(request, 'vol/detail.html', {'vol': vol})

def somme(request):
#    vol = Vol.objects.all()
    avions = TypeAvion.objects.all()

    liste_somme_vols_cur_year = []
    liste_somme_vols_last_year = []
    liste_somme_vols_total = []

    for modele_avion in avions:
        # Current Year
        somme_vols_jour_cdb = Vol.objects.filter(poste="CDB", immatriculation__type_avion__type_avion=modele_avion).aggregate(Sum('duree_jour'))
        somme_vols_nuit_cdb = Vol.objects.filter(poste="CDB", immatriculation__type_avion__type_avion=modele_avion).aggregate(Sum('duree_nuit'))
        somme_vols_jour_opl = Vol.objects.filter(poste="OPL", immatriculation__type_avion__type_avion=modele_avion).aggregate(Sum('duree_jour'))
        somme_vols_nuit_opl = Vol.objects.filter(poste="OPL", immatriculation__type_avion__type_avion=modele_avion).aggregate(Sum('duree_nuit'))
        
        liste_somme_vols_cur_year.append([modele_avion, somme_vols_jour_cdb,somme_vols_nuit_cdb,somme_vols_jour_opl,somme_vols_nuit_opl])

        # Last Year
        somme_vols_jour_cdb = Vol.objects.filter(poste="CDB", immatriculation__type_avion__type_avion=modele_avion).aggregate(Sum('duree_jour'))
        somme_vols_nuit_cdb = Vol.objects.filter(poste="CDB", immatriculation__type_avion__type_avion=modele_avion).aggregate(Sum('duree_nuit'))
        somme_vols_jour_opl = Vol.objects.filter(poste="OPL", immatriculation__type_avion__type_avion=modele_avion).aggregate(Sum('duree_jour'))
        somme_vols_nuit_opl = Vol.objects.filter(poste="OPL", immatriculation__type_avion__type_avion=modele_avion).aggregate(Sum('duree_nuit'))
        
        liste_somme_vols_last_year.append([modele_avion, somme_vols_jour_cdb,somme_vols_nuit_cdb,somme_vols_jour_opl,somme_vols_nuit_opl])

        # Total Year
        somme_vols_jour_cdb = Vol.objects.filter(poste="CDB", immatriculation__type_avion__type_avion=modele_avion).aggregate(Sum('duree_jour'))
        somme_vols_nuit_cdb = Vol.objects.filter(poste="CDB", immatriculation__type_avion__type_avion=modele_avion).aggregate(Sum('duree_nuit'))
        somme_vols_jour_opl = Vol.objects.filter(poste="OPL", immatriculation__type_avion__type_avion=modele_avion).aggregate(Sum('duree_jour'))
        somme_vols_nuit_opl = Vol.objects.filter(poste="OPL", immatriculation__type_avion__type_avion=modele_avion).aggregate(Sum('duree_nuit'))
        
        liste_somme_vols_total.append([modele_avion, somme_vols_jour_cdb,somme_vols_nuit_cdb,somme_vols_jour_opl,somme_vols_nuit_opl])
        



    data = {
#        'avions':avions,
#        'somme_vols_jours': somme_vols_jours,
#        'somme_vols_nuit': somme_vols_nuit,
#        'somme_vols_jour_cdb': somme_vols_jour_cdb,
#        'somme_vols_nuit_cdb': somme_vols_nuit_cdb,
#        'liste_somme_vols_jour_cdb_type_avion': liste_somme_vols_jour_cdb_type_avion,
        'liste_somme_vols_cur_year': liste_somme_vols_cur_year,
        'liste_somme_vols_last_year': liste_somme_vols_last_year,
        'liste_somme_vols_total': liste_somme_vols_total,
#        'liste_somme_vols_nuit_cdb_type_avion': liste_somme_vols_nuit_cdb_type_avion,
#        'liste_somme_vols_jour_opl_type_avion': liste_somme_vols_jour_opl_type_avion,
#        'liste_somme_vols_nuit_opl_type_avion': liste_somme_vols_nuit_opl_type_avion,
#        'liste_somme_vols_type_avion': liste_somme_vols_type_avion,
    }

    return render(request, 'vol/somme.html', {'data': data})