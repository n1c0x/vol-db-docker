from django.shortcuts import render,get_object_or_404
from django.db.models import Sum
from django.http import HttpResponse
import datetime

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
        current_year = datetime.datetime.now()
        somme_vols_jour_cdb_cur_year = Vol.objects.filter(poste="CDB", immatriculation__type_avion__type_avion=modele_avion,date__year=current_year.year).aggregate(Sum('duree_jour'))
        somme_vols_nuit_cdb_cur_year = Vol.objects.filter(poste="CDB", immatriculation__type_avion__type_avion=modele_avion,date__year=current_year.year).aggregate(Sum('duree_nuit'))
        somme_vols_jour_opl_cur_year = Vol.objects.filter(poste="OPL", immatriculation__type_avion__type_avion=modele_avion,date__year=current_year.year).aggregate(Sum('duree_jour'))
        somme_vols_nuit_opl_cur_year = Vol.objects.filter(poste="OPL", immatriculation__type_avion__type_avion=modele_avion,date__year=current_year.year).aggregate(Sum('duree_nuit'))
        somme_vols_jour_inst_cur_year = Vol.objects.filter(poste="Instruct", immatriculation__type_avion__type_avion=modele_avion,date__year=current_year.year).aggregate(Sum('duree_jour'))
        somme_vols_nuit_inst_cur_year = Vol.objects.filter(poste="Instruct", immatriculation__type_avion__type_avion=modele_avion,date__year=current_year.year).aggregate(Sum('duree_nuit'))

        # Last Year
        somme_vols_jour_cdb_last_year = Vol.objects.filter(poste="CDB", immatriculation__type_avion__type_avion=modele_avion,date__year=current_year.year-1).aggregate(Sum('duree_jour'))
        somme_vols_nuit_cdb_last_year = Vol.objects.filter(poste="CDB", immatriculation__type_avion__type_avion=modele_avion,date__year=current_year.year-1).aggregate(Sum('duree_nuit'))
        somme_vols_jour_opl_last_year = Vol.objects.filter(poste="OPL", immatriculation__type_avion__type_avion=modele_avion,date__year=current_year.year-1).aggregate(Sum('duree_jour'))
        somme_vols_nuit_opl_last_year = Vol.objects.filter(poste="OPL", immatriculation__type_avion__type_avion=modele_avion,date__year=current_year.year-1).aggregate(Sum('duree_nuit'))
        somme_vols_jour_inst_last_year = Vol.objects.filter(poste="Instruct", immatriculation__type_avion__type_avion=modele_avion,date__year=current_year.year-1).aggregate(Sum('duree_jour'))
        somme_vols_nuit_inst_last_year = Vol.objects.filter(poste="Instruct", immatriculation__type_avion__type_avion=modele_avion,date__year=current_year.year-1).aggregate(Sum('duree_nuit'))

        # Total Year
        somme_vols_jour_cdb_total = Vol.objects.filter(poste="CDB", immatriculation__type_avion__type_avion=modele_avion).aggregate(Sum('duree_jour'))
        somme_vols_nuit_cdb_total = Vol.objects.filter(poste="CDB", immatriculation__type_avion__type_avion=modele_avion).aggregate(Sum('duree_nuit'))
        somme_vols_jour_opl_total = Vol.objects.filter(poste="OPL", immatriculation__type_avion__type_avion=modele_avion).aggregate(Sum('duree_jour'))
        somme_vols_nuit_opl_total = Vol.objects.filter(poste="OPL", immatriculation__type_avion__type_avion=modele_avion).aggregate(Sum('duree_nuit'))
        somme_vols_jour_inst_total = Vol.objects.filter(poste="Instruct", immatriculation__type_avion__type_avion=modele_avion).aggregate(Sum('duree_jour'))
        somme_vols_nuit_inst_total = Vol.objects.filter(poste="Instruct", immatriculation__type_avion__type_avion=modele_avion).aggregate(Sum('duree_nuit'))

        liste_somme_vols_total.append([
            modele_avion, 
            somme_vols_jour_cdb_cur_year,
            somme_vols_nuit_cdb_cur_year,
            somme_vols_jour_opl_cur_year,
            somme_vols_nuit_opl_cur_year,
            somme_vols_jour_cdb_last_year,
            somme_vols_nuit_cdb_last_year,
            somme_vols_jour_opl_last_year,
            somme_vols_nuit_opl_last_year,
            somme_vols_jour_cdb_total,
            somme_vols_nuit_cdb_total,
            somme_vols_jour_opl_total,
            somme_vols_nuit_opl_total,
            somme_vols_jour_inst_cur_year,
            somme_vols_nuit_inst_cur_year,
            somme_vols_jour_inst_last_year,
            somme_vols_nuit_inst_last_year,
            somme_vols_jour_inst_total,
            somme_vols_nuit_inst_total,
            ])
        



    data = {
        'liste_somme_vols_cur_year': liste_somme_vols_cur_year,
        'liste_somme_vols_last_year': liste_somme_vols_last_year,
        'liste_somme_vols_total': liste_somme_vols_total,
    }

    return render(request, 'vol/somme.html', {'data': data})