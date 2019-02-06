from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, When
from .forms import VolForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


from datetime import date, datetime, timedelta

from .models import Vol, Immatriculation, TypeAvion

def homepage(request):
    return render(request, 'vol/homepage.html')

def prices(request):
    return render(request, 'vol/prices.html')

@login_required
def get_user_profile(request, username):
    user = User.objects.get(username=username)
    return render(request, 'vol/profile.html', {"user":user})

@login_required
def index(request):
    vols_list = Vol.objects.order_by('-date')
    context = {
        'vols_list': vols_list
    }
    return render(request, 'vol/index.html', context)

@login_required
def detail(request, vol_id):
    vol = get_object_or_404(Vol, pk=vol_id)
    return render(request, 'vol/detail.html', {'vol': vol})

@login_required
def somme(request):
#    vol = Vol.objects.all()
    avions = TypeAvion.objects.all()

    liste_somme_vols_cur_year = []
    liste_somme_vols_last_year = []
    liste_somme_vols_total = []
    liste_somme_vols_total_total = []

    for modele_avion in avions:
        
        today = date.today()
        current_year = datetime(today.year, 1, 1)
        
        # Current Year
        somme_vols_jour_cdb_cur_year = Vol.objects.filter(poste="CDB", immatriculation__type_avion__type_avion=modele_avion, date__year=current_year.year).aggregate(Sum('duree_jour'))
        somme_vols_nuit_cdb_cur_year = Vol.objects.filter(poste="CDB", immatriculation__type_avion__type_avion=modele_avion, date__year=current_year.year).aggregate(Sum('duree_nuit'))
        somme_vols_jour_opl_cur_year = Vol.objects.filter(poste="OPL", immatriculation__type_avion__type_avion=modele_avion, date__year=current_year.year).aggregate(Sum('duree_jour'))
        somme_vols_nuit_opl_cur_year = Vol.objects.filter(poste="OPL", immatriculation__type_avion__type_avion=modele_avion, date__year=current_year.year).aggregate(Sum('duree_nuit'))
        somme_vols_jour_inst_cur_year = Vol.objects.filter(poste="Instruct", immatriculation__type_avion__type_avion=modele_avion, date__year=current_year.year).aggregate(Sum('duree_jour'))
        somme_vols_nuit_inst_cur_year = Vol.objects.filter(poste="Instruct", immatriculation__type_avion__type_avion=modele_avion, date__year=current_year.year).aggregate(Sum('duree_nuit'))
        somme_vols_simu_cur_year = Vol.objects.filter(immatriculation__type_avion__type_avion=modele_avion, date__year=current_year.year).aggregate(Sum('duree_simu'))
        somme_vols_arrivee_ifr_cur_year = Vol.objects.filter(immatriculation__type_avion__type_avion=modele_avion, date__year=current_year.year).aggregate(Sum('vol_ifr'))

        print(somme_vols_arrivee_ifr_cur_year)

        # Last Year
        somme_vols_jour_cdb_last_year = Vol.objects.filter(poste="CDB", immatriculation__type_avion__type_avion=modele_avion).exclude(date__gt=current_year).aggregate(Sum('duree_jour'))
        somme_vols_nuit_cdb_last_year = Vol.objects.filter(poste="CDB", immatriculation__type_avion__type_avion=modele_avion).exclude(date__gt=current_year).aggregate(Sum('duree_nuit'))
        somme_vols_jour_opl_last_year = Vol.objects.filter(poste="OPL", immatriculation__type_avion__type_avion=modele_avion).exclude(date__gt=current_year).aggregate(Sum('duree_jour'))
        somme_vols_nuit_opl_last_year = Vol.objects.filter(poste="OPL", immatriculation__type_avion__type_avion=modele_avion).exclude(date__gt=current_year).aggregate(Sum('duree_nuit'))
        somme_vols_jour_inst_last_year = Vol.objects.filter(poste="Instruct", immatriculation__type_avion__type_avion=modele_avion).exclude(date__gt=current_year).aggregate(Sum('duree_jour'))
        somme_vols_nuit_inst_last_year = Vol.objects.filter(poste="Instruct", immatriculation__type_avion__type_avion=modele_avion).exclude(date__gt=current_year).aggregate(Sum('duree_nuit'))
        somme_vols_simu_last_year = Vol.objects.filter(immatriculation__type_avion__type_avion=modele_avion).exclude(date__gt=current_year).aggregate(Sum('duree_simu'))
        somme_vols_arrivee_ifr_last_year = Vol.objects.filter(immatriculation__type_avion__type_avion=modele_avion).exclude(date__gt=current_year).aggregate(Sum('vol_ifr'))

        print(somme_vols_arrivee_ifr_cur_year)

        # Total Year
        somme_vols_jour_cdb_total = Vol.objects.filter(poste="CDB", immatriculation__type_avion__type_avion=modele_avion).aggregate(Sum('duree_jour'))
        somme_vols_nuit_cdb_total = Vol.objects.filter(poste="CDB",  immatriculation__type_avion__type_avion=modele_avion).aggregate(Sum('duree_nuit'))
        somme_vols_jour_opl_total = Vol.objects.filter(poste="OPL", immatriculation__type_avion__type_avion=modele_avion).aggregate(Sum('duree_jour'))
        somme_vols_nuit_opl_total = Vol.objects.filter(poste="OPL", immatriculation__type_avion__type_avion=modele_avion).aggregate(Sum('duree_nuit'))
        somme_vols_jour_inst_total = Vol.objects.filter(poste="Instruct", immatriculation__type_avion__type_avion=modele_avion).aggregate(Sum('duree_jour'))
        somme_vols_nuit_inst_total = Vol.objects.filter(poste="Instruct", immatriculation__type_avion__type_avion=modele_avion).aggregate(Sum('duree_nuit'))

        somme_vols_jour_dc_cur_year = []
        somme_vols_nuit_dc_cur_year = []
        somme_vols_jour_dc_last_year = []
        somme_vols_nuit_dc_last_year = []
        somme_vols_jour_dc_total = []
        somme_vols_nuit_dc_total = []

        if somme_vols_jour_cdb_cur_year["duree_jour__sum"] is None:
            somme_vols_jour_cdb_cur_year["duree_jour__sum"] = timedelta(0)
        if somme_vols_nuit_cdb_cur_year["duree_nuit__sum"] is None:
            somme_vols_nuit_cdb_cur_year["duree_nuit__sum"] = timedelta(0)
        if somme_vols_jour_opl_cur_year["duree_jour__sum"] is None:
            somme_vols_jour_opl_cur_year["duree_jour__sum"] = timedelta(0)
        if somme_vols_nuit_opl_cur_year["duree_nuit__sum"] is None:
            somme_vols_nuit_opl_cur_year["duree_nuit__sum"] = timedelta(0)
#        if somme_vols_jour_dc_cur_year["duree_jour__sum"] is None:
#            somme_vols_jour_dc_cur_year["duree_jour__sum"] = datetime.timedelta(0)
#        if somme_vols_nuit_dc_cur_year["duree_nuit__sum"] is None:
#            somme_vols_nuit_dc_cur_year["duree_nuit__sum"] = datetime.timedelta(0)
        if somme_vols_jour_inst_cur_year["duree_jour__sum"] is None:
            somme_vols_jour_inst_cur_year["duree_jour__sum"] = timedelta(0)
        if somme_vols_nuit_inst_cur_year["duree_nuit__sum"] is None:
            somme_vols_nuit_inst_cur_year["duree_nuit__sum"] = timedelta(0)
        if somme_vols_simu_cur_year["duree_simu__sum"] is None:
            somme_vols_simu_cur_year["duree_simu__sum"] = timedelta(0)
        if somme_vols_jour_cdb_last_year["duree_jour__sum"] is None:
            somme_vols_jour_cdb_last_year["duree_jour__sum"] = timedelta(0)
        if somme_vols_nuit_cdb_last_year["duree_nuit__sum"] is None:
            somme_vols_nuit_cdb_last_year["duree_nuit__sum"] = timedelta(0)
        if somme_vols_jour_opl_last_year["duree_jour__sum"] is None:
            somme_vols_jour_opl_last_year["duree_jour__sum"] = timedelta(0)
        if somme_vols_nuit_opl_last_year["duree_nuit__sum"] is None:
            somme_vols_nuit_opl_last_year["duree_nuit__sum"] = timedelta(0)
#        if somme_vols_jour_dc_last_year["duree_jour__sum"] is None:
#            somme_vols_jour_dc_last_year["duree_jour__sum"] = datetime.timedelta(0)
#        if somme_vols_nuit_dc_last_year["duree_nuit__sum"] is None:
#            somme_vols_nuit_dc_last_year["duree_nuit__sum"] = datetime.timedelta(0)
        if somme_vols_jour_inst_last_year["duree_jour__sum"] is None:
            somme_vols_jour_inst_last_year["duree_jour__sum"] = timedelta(0)
        if somme_vols_nuit_inst_last_year["duree_nuit__sum"] is None:
            somme_vols_nuit_inst_last_year["duree_nuit__sum"] = timedelta(0)
        if somme_vols_simu_last_year["duree_simu__sum"] is None:
            somme_vols_simu_last_year["duree_simu__sum"] = timedelta(0)
        if somme_vols_jour_cdb_total["duree_jour__sum"] is None:
            somme_vols_jour_cdb_total["duree_jour__sum"] = timedelta(0)
        if somme_vols_nuit_cdb_total["duree_nuit__sum"] is None:
            somme_vols_nuit_cdb_total["duree_nuit__sum"] = timedelta(0)
        if somme_vols_jour_opl_total["duree_jour__sum"] is None:
            somme_vols_jour_opl_total["duree_jour__sum"] = timedelta(0)
        if somme_vols_nuit_opl_total["duree_nuit__sum"] is None:
            somme_vols_nuit_opl_total["duree_nuit__sum"] = timedelta(0)
#        if somme_vols_jour_dc_total["duree_jour__sum"] is None:
#            somme_vols_jour_dc_total["duree_jour__sum"] = datetime.timedelta(0)
#        if somme_vols_nuit_dc_total["duree_nuit__sum"] is None:
#            somme_vols_nuit_dc_total["duree_nuit__sum"] = datetime.timedelta(0)
        if somme_vols_jour_inst_total["duree_jour__sum"] is None:
            somme_vols_jour_inst_total["duree_jour__sum"] = timedelta(0)
        if somme_vols_nuit_inst_total["duree_nuit__sum"] is None:
            somme_vols_nuit_inst_total["duree_nuit__sum"] = timedelta(0)


        # Total de tous les vols
        liste_somme_vols_cur_year = somme_vols_jour_cdb_cur_year["duree_jour__sum"] + somme_vols_nuit_cdb_cur_year["duree_nuit__sum"] + somme_vols_jour_opl_cur_year["duree_jour__sum"] + somme_vols_nuit_opl_cur_year["duree_nuit__sum"] + somme_vols_jour_inst_cur_year["duree_jour__sum"] + somme_vols_nuit_inst_cur_year["duree_nuit__sum"]

        liste_somme_vols_last_year = somme_vols_jour_cdb_last_year["duree_jour__sum"] + somme_vols_nuit_cdb_last_year["duree_nuit__sum"] + somme_vols_jour_opl_last_year["duree_jour__sum"] + somme_vols_nuit_opl_last_year["duree_nuit__sum"] + somme_vols_jour_inst_last_year["duree_jour__sum"] + somme_vols_nuit_inst_last_year["duree_nuit__sum"]

        liste_somme_vols_total_total = somme_vols_jour_cdb_total["duree_jour__sum"] + somme_vols_nuit_cdb_total["duree_nuit__sum"] + somme_vols_jour_opl_total["duree_jour__sum"] + somme_vols_nuit_opl_total["duree_nuit__sum"] + somme_vols_jour_inst_total["duree_jour__sum"] + somme_vols_nuit_inst_total["duree_nuit__sum"]

        liste_somme_vols_total.append([
            modele_avion, 
            somme_vols_jour_cdb_cur_year,
            somme_vols_nuit_cdb_cur_year,
            somme_vols_jour_opl_cur_year,
            somme_vols_nuit_opl_cur_year,
            somme_vols_jour_dc_cur_year,
            somme_vols_nuit_dc_cur_year,
            somme_vols_jour_inst_cur_year,
            somme_vols_nuit_inst_cur_year,
            somme_vols_jour_cdb_last_year,
            somme_vols_nuit_cdb_last_year,
            somme_vols_jour_opl_last_year,
            somme_vols_nuit_opl_last_year,
            somme_vols_jour_dc_last_year,
            somme_vols_nuit_dc_last_year,
            somme_vols_jour_inst_last_year,
            somme_vols_nuit_inst_last_year,
            somme_vols_jour_cdb_total,
            somme_vols_nuit_cdb_total,
            somme_vols_jour_opl_total,
            somme_vols_nuit_opl_total,
            somme_vols_jour_dc_total,
            somme_vols_nuit_dc_total,
            somme_vols_jour_inst_total,
            somme_vols_nuit_inst_total,
            liste_somme_vols_cur_year,
            liste_somme_vols_last_year,
            liste_somme_vols_total_total,
            somme_vols_simu_cur_year,
            somme_vols_simu_last_year,
            somme_vols_arrivee_ifr_cur_year,
            somme_vols_arrivee_ifr_last_year,
            ])


    data = {
        'liste_somme_vols_cur_year': liste_somme_vols_cur_year,
        'liste_somme_vols_last_year': liste_somme_vols_last_year,
        'liste_somme_vols_total': liste_somme_vols_total,
    }

    return render(request, 'vol/somme.html', {'data': data})

@login_required
def new_vol(request):
    if request.method == "POST":
        form = VolForm(request.POST)
        if form.is_valid():
            vol = form.save(commit=False)
            vol.save()
            return redirect('index')
    else:
        form = VolForm()
    return render(request, 'vol/vol_add.html', {'form': form})

@login_required
def edit_vol(request, pk):
    vol = get_object_or_404(Vol, pk=pk)
    if request.method == "POST":
        form = VolForm(request.POST, instance=vol)
        if form.is_valid():
            vol = form.save(commit=False)
            vol.save()
            return redirect('index')
    else:
        form = VolForm(instance=vol)
    return render(request, 'vol/vol_add.html', {'form': form})

@login_required
def remove_vol(request, pk):
    vol = get_object_or_404(Vol, pk=pk)
    vol.delete()
    return redirect('index')
