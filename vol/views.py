from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from .forms import *
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
    return render(request, 'vol/profile.html', {"user": user})


@login_required
def index(request):
    current_user = request.user
    vols_list = Vol.objects.order_by('-date').filter(user_id=current_user.id)
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
    current_user = request.user
    avions = TypeAvion.objects.all()

    liste_somme_vols_cur_year = []
    liste_somme_vols_last_year = []
    liste_somme_vols_total = []
    liste_somme_vols_total_total = []

    for modele_avion in avions:

        today = date.today()
        current_year = datetime(today.year, 1, 1)

        # Current Year
        somme_vols_jour_cdb_cur_year = Vol.objects.filter(
            poste="CDB",
            immatriculation__type_avion__type_avion=modele_avion,
            date__year=current_year.year,
            user_id=current_user.id).aggregate(Sum('duree_jour'))
        somme_vols_nuit_cdb_cur_year = Vol.objects.filter(
            poste="CDB",
            immatriculation__type_avion__type_avion=modele_avion,
            date__year=current_year.year,
            user_id=current_user.id).aggregate(Sum('duree_nuit'))
        somme_vols_jour_opl_cur_year = Vol.objects.filter(
            poste="OPL",
            immatriculation__type_avion__type_avion=modele_avion,
            date__year=current_year.year,
            user_id=current_user.id).aggregate(Sum('duree_jour'))
        somme_vols_nuit_opl_cur_year = Vol.objects.filter(
            poste="OPL",
            immatriculation__type_avion__type_avion=modele_avion,
            date__year=current_year.year,
            user_id=current_user.id).aggregate(Sum('duree_nuit'))
        somme_vols_jour_inst_cur_year = Vol.objects.filter(
            poste="Instruct",
            immatriculation__type_avion__type_avion=modele_avion,
            date__year=current_year.year,
            user_id=current_user.id).aggregate(Sum('duree_jour'))
        somme_vols_nuit_inst_cur_year = Vol.objects.filter(
            poste="Instruct",
            immatriculation__type_avion__type_avion=modele_avion,
            date__year=current_year.year,
            user_id=current_user.id).aggregate(Sum('duree_nuit'))
        somme_vols_simu_cur_year = Vol.objects.filter(
            immatriculation__type_avion__type_avion=modele_avion,
            date__year=current_year.year,
            user_id=current_user.id).aggregate(Sum('duree_simu'))
        somme_vols_arrivee_ifr_cur_year = Vol.objects.filter(immatriculation__type_avion__type_avion=modele_avion, date__year=current_year.year, user_id=current_user.id).aggregate(Sum('vol_ifr'))

        # Last Year
        somme_vols_jour_cdb_last_year = Vol.objects.filter(
            poste="CDB",
            immatriculation__type_avion__type_avion=modele_avion,
            user_id=current_user.id).exclude(date__gt=current_year).aggregate(Sum('duree_jour'))
        somme_vols_nuit_cdb_last_year = Vol.objects.filter(
            poste="CDB",
            immatriculation__type_avion__type_avion=modele_avion,
            user_id=current_user.id).exclude(date__gt=current_year).aggregate(Sum('duree_nuit'))
        somme_vols_jour_opl_last_year = Vol.objects.filter(
            poste="OPL",
            immatriculation__type_avion__type_avion=modele_avion,
            user_id=current_user.id).exclude(date__gt=current_year).aggregate(Sum('duree_jour'))
        somme_vols_nuit_opl_last_year = Vol.objects.filter(
            poste="OPL",
            immatriculation__type_avion__type_avion=modele_avion,
            user_id=current_user.id).exclude(date__gt=current_year).aggregate(Sum('duree_nuit'))
        somme_vols_jour_inst_last_year = Vol.objects.filter(
            poste="Instruct",
            immatriculation__type_avion__type_avion=modele_avion,
            user_id=current_user.id).exclude(date__gt=current_year).aggregate(Sum('duree_jour'))
        somme_vols_nuit_inst_last_year = Vol.objects.filter(
            poste="Instruct",
            immatriculation__type_avion__type_avion=modele_avion,
            user_id=current_user.id).exclude(date__gt=current_year).aggregate(Sum('duree_nuit'))
        somme_vols_simu_last_year = Vol.objects.filter(
            immatriculation__type_avion__type_avion=modele_avion,
            user_id=current_user.id).exclude(date__gt=current_year).aggregate(Sum('duree_simu'))
        somme_vols_arrivee_ifr_last_year = Vol.objects.filter(immatriculation__type_avion__type_avion=modele_avion, user_id=current_user.id).exclude(date__gt=current_year).aggregate(Sum('vol_ifr'))

        # Total Year
        somme_vols_jour_cdb_total = Vol.objects.filter(
            poste="CDB",
            immatriculation__type_avion__type_avion=modele_avion,
            user_id=current_user.id).aggregate(Sum('duree_jour'))
        somme_vols_nuit_cdb_total = Vol.objects.filter(
            poste="CDB",
            immatriculation__type_avion__type_avion=modele_avion,
            user_id=current_user.id).aggregate(Sum('duree_nuit'))
        somme_vols_jour_opl_total = Vol.objects.filter(
            poste="OPL",
            immatriculation__type_avion__type_avion=modele_avion,
            user_id=current_user.id).aggregate(Sum('duree_jour'))
        somme_vols_nuit_opl_total = Vol.objects.filter(
            poste="OPL",
            immatriculation__type_avion__type_avion=modele_avion,
            user_id=current_user.id).aggregate(Sum('duree_nuit'))
        somme_vols_jour_inst_total = Vol.objects.filter(
            poste="Instruct",
            immatriculation__type_avion__type_avion=modele_avion,
            user_id=current_user.id).aggregate(Sum('duree_jour'))
        somme_vols_nuit_inst_total = Vol.objects.filter(
            poste="Instruct",
            immatriculation__type_avion__type_avion=modele_avion,
            user_id=current_user.id).aggregate(Sum('duree_nuit'))

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
        liste_somme_vols_cur_year = somme_vols_jour_cdb_cur_year["duree_jour__sum"] +somme_vols_nuit_cdb_cur_year["duree_nuit__sum"] + somme_vols_jour_opl_cur_year["duree_jour__sum"] + somme_vols_nuit_opl_cur_year["duree_nuit__sum"] + somme_vols_jour_inst_cur_year["duree_jour__sum"] + somme_vols_nuit_inst_cur_year["duree_nuit__sum"]

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
        form_vol = VolForm(request.POST)
        if form_vol.is_valid():
            vol = form_vol.save(commit=False)
            vol.user_id = request.user
            vol.save()
            return redirect('index')
    else:
        form_vol = VolForm()
    return render(request, 'vol/vol_add.html', {'form': form_vol})


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


@login_required
def new_immatriculation(request):
    current_user = request.user
    immatriculation_list = Immatriculation.objects.order_by('immatriculation').filter(user_id=current_user.id)
    if request.method == "POST":
        form_immatriculation = ImmatriculationForm(request.POST)
        if form_immatriculation.is_valid():
            immatriculation = form_immatriculation.save(commit=False)
            immatriculation.user_id = request.user
            immatriculation.save()
            return redirect('new_immatriculation')
    else:
        form_immatriculation = ImmatriculationForm()
    context = {
        'immatriculation_list': immatriculation_list,
        'form_immatriculation': form_immatriculation,
    }
    return render(
        request,
        'vol/immatriculation_add.html',
        context)


@login_required
def edit_immatriculation(request, pk):
    current_user = request.user
    immatriculation_list = Immatriculation.objects.order_by('immatriculation').filter(user_id=current_user.id)
    immatriculation = get_object_or_404(Immatriculation, pk=pk)
    if request.method == "POST":
        form_immatriculation = ImmatriculationForm(request.POST, instance=immatriculation)
        if form_immatriculation.is_valid():
            immatriculation = form_immatriculation.save(commit=False)
            immatriculation.save()
            return redirect('new_immatriculation')
    else:
        form_immatriculation = ImmatriculationForm(instance=immatriculation)
    context = {
        'immatriculation_list': immatriculation_list,
        'form_immatriculation': form_immatriculation,
    }
    return render(
        request,
        'vol/immatriculation_add.html',
        context)


@login_required
def remove_immatriculation(request, pk):
    immatriculation = get_object_or_404(Immatriculation, pk=pk)
    immatriculation.delete()
    return redirect('new_immatriculation')


@login_required
def new_pilote(request):
    current_user = request.user
    pilotes_list = Pilote.objects.order_by('nom').filter(user_id=current_user.id)
    if request.method == "POST":
        form_pilote = PiloteForm(request.POST)
        if form_pilote.is_valid():
            pilote = form_pilote.save(commit=False)
            pilote.user_id = request.user
            pilote.save()
            return redirect('new_pilot')
    else:
        form_pilote = PiloteForm()
    context = {
        'pilotes_list': pilotes_list,
        'form_pilote': form_pilote,
    }
    return render(
        request,
        'vol/pilote_add.html',
        context)


@login_required
def edit_pilote(request, pk):
    current_user = request.user
    pilotes_list = Pilote.objects.order_by('nom').filter(user_id=current_user.id)
    pilote = get_object_or_404(Pilote, pk=pk)
    if request.method == "POST":
        form_pilote = PiloteForm(request.POST, instance=pilote)
        if form_pilote.is_valid():
            pilote = form_pilote.save(commit=False)
            pilote.save()
            return redirect('new_pilote')
    else:
        form_pilote = PiloteForm(instance=pilote)
    context = {
        'pilotes_list': pilotes_list,
        'form_pilote': form_pilote,
    }
    return render(
        request,
        'vol/pilote_add.html',
        context)


@login_required
def remove_pilote(request, pk):
    pilote = get_object_or_404(Pilote, pk=pk)
    pilote.delete()
    return redirect('pilote_add')


@login_required
def new_iata(request):
    current_user = request.user
    iata_list = CodeIata.objects.order_by('code_iata').filter(user_id=current_user.id)
    if request.method == "POST":
        form_iata = IataForm(request.POST)
        if form_iata.is_valid():
            iata = form_iata.save(commit=False)
            iata.user_id = request.user
            iata.save()
            return redirect('new_iata')
    else:
        form_iata = IataForm()
    context = {
        'iata_list': iata_list,
        'form_iata': form_iata,
    }
    return render(
        request,
        'vol/iata_add.html',
        context)


@login_required
def edit_iata(request, pk):
    current_user = request.user
    iata_list = CodeIata.objects.order_by('code_iata').filter(user_id=current_user.id)
    iata = get_object_or_404(CodeIata, pk=pk)
    if request.method == "POST":
        form_iata = IataForm(request.POST, instance=iata)
        if form_iata.is_valid():
            iata = form_iata.save(commit=False)
            iata.save()
            return redirect('new_iata')
    else:
        form_iata = IataForm(instance=iata)
    context = {
        'iata_list': iata_list,
        'form_iata': form_iata,
    }
    return render(
        request,
        'vol/iata_add.html',
        context)


@login_required
def remove_iata(request, pk):
    iata = get_object_or_404(CodeIata, pk=pk)
    iata.delete()
    return redirect('new_iata')


@login_required
def new_type_avion(request):
    current_user = request.user
    type_avion_list = TypeAvion.objects.order_by('type_avion').filter(user_id=current_user.id)
    if request.method == "POST":
        form_type_avion = TypeAvionForm(request.POST)
        if form_type_avion.is_valid():
            type_avion = form_type_avion.save(commit=False)
            type_avion.user_id = request.user
            type_avion.save()
            return redirect('new_type_avion')
    else:
        form_type_avion = TypeAvionForm()
    context = {
        'type_avion_list': type_avion_list,
        'form_type_avion': form_type_avion,
    }
    return render(
        request,
        'vol/type_avion_add.html',
        context)


@login_required
def edit_type_avion(request, pk):
    current_user = request.user
    type_avion_list = TypeAvion.objects.order_by('type_avion').filter(user_id=current_user.id)
    type_avion = get_object_or_404(TypeAvion, pk=pk)
    if request.method == "POST":
        form_type_avion = TypeAvionForm(request.POST, instance=type_avion)
        if form_type_avion.is_valid():
            type_avion = form_type_avion.save(commit=False)
            type_avion.save()
            return redirect('new_type_avion')
    else:
        form_type_avion = TypeAvionForm(instance=type_avion)
    context = {
        'type_avion_list': type_avion_list,
        'form_type_avion': form_type_avion,
    }
    return render(
        request,
        'vol/type_avion_add.html',
        context)


@login_required
def remove_type_avion(request, pk):
    type_avion = get_object_or_404(TypeAvion, pk=pk)
    type_avion.delete()
    return redirect('new_type_avion')
