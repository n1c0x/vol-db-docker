from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from .forms import *
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from datetime import date, datetime, timedelta
from .models import *

from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator


def homepage(request):
    """ Render the home page. """
    return render(request, 'vol/homepage.html')


def prices(request):
    """ Render de prices page. """
    return render(request, 'vol/prices.html')


@login_required
def get_user_profile(request, username):
    """ Render the current user profile on the profile page. """
    user = User.objects.get(username=username)
    return render(request, 'vol/profile.html', {"user": user})


@login_required
def update_user_profile(request, username):
    is_modified = True
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            profile_form = profile_form.save(commit=False)
            for x in Profile.objects.all():
                profile_form.client_type = x.client_type
            user_form.save()
            profile_form.save()
            return redirect('profile', username=username)
        # else:
        #     return render(request, 'vol/error_not_allowed.html')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'vol/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'is_modified': is_modified,
    })


@method_decorator(login_required, name='dispatch')
class VolList(ListView):
    model = Vol
    template_name = 'vol/index.html'

    def get_queryset(self):
        return Vol.objects.order_by('-date').filter(user_id=self.request.user)

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@method_decorator(login_required, name='dispatch')
class VolDetail(DetailView):
    model = Vol
    template_name = 'vol/detail.html'
    # vol = Vol.objects.filter(user_id=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(VolDetail, self).get_context_data(**kwargs)
        vols_list = Vol.objects.filter(user_id=self.request.user)
        vol = get_object_or_404(vols_list, pk=self.kwargs.get('pk', None))
        context['vol'] = vol
        return context

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@login_required
def somme(request):
    """
        Render the sum page. This page displays the sums of all the flights
        grouped by plane type, year and function.
    """
    current_user = request.user
    # avions = TypeAvion.objects.all()
    avions = TypeAvion.objects.filter(user_id=current_user.id)

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
        somme_vols_arrivee_ifr_cur_year = Vol.objects.filter(
            immatriculation__type_avion__type_avion=modele_avion,
            date__year=current_year.year,
            user_id=current_user.id,
            vol_ifr__gt=0).aggregate(Sum('vol_ifr'))

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
        somme_vols_arrivee_ifr_last_year = Vol.objects.filter(
            immatriculation__type_avion__type_avion=modele_avion,
            user_id=current_user.id,
            vol_ifr__gt=0).exclude(date__gt=current_year).aggregate(Sum('vol_ifr'))

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
        somme_vols_arrivee_ifr_total = Vol.objects.filter(
            immatriculation__type_avion__type_avion=modele_avion,
            user_id=current_user.id,
            vol_ifr__gt=0).aggregate(Sum('vol_ifr'))

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
        # if somme_vols_jour_dc_cur_year["duree_jour__sum"] is None:
        #     somme_vols_jour_dc_cur_year["duree_jour__sum"] = datetime.timedelta(0)
        # if somme_vols_nuit_dc_cur_year["duree_nuit__sum"] is None:
        #     somme_vols_nuit_dc_cur_year["duree_nuit__sum"] = datetime.timedelta(0)
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
       # if somme_vols_jour_dc_last_year["duree_jour__sum"] is None:
       #     somme_vols_jour_dc_last_year["duree_jour__sum"] = datetime.timedelta(0)
       # if somme_vols_nuit_dc_last_year["duree_nuit__sum"] is None:
       #     somme_vols_nuit_dc_last_year["duree_nuit__sum"] = datetime.timedelta(0)
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
       # if somme_vols_jour_dc_total["duree_jour__sum"] is None:
       #     somme_vols_jour_dc_total["duree_jour__sum"] = datetime.timedelta(0)
       # if somme_vols_nuit_dc_total["duree_nuit__sum"] is None:
       #     somme_vols_nuit_dc_total["duree_nuit__sum"] = datetime.timedelta(0)
        if somme_vols_jour_inst_total["duree_jour__sum"] is None:
            somme_vols_jour_inst_total["duree_jour__sum"] = timedelta(0)
        if somme_vols_nuit_inst_total["duree_nuit__sum"] is None:
            somme_vols_nuit_inst_total["duree_nuit__sum"] = timedelta(0)

        # Total de tous les vols
        liste_somme_vols_cur_year = somme_vols_jour_cdb_cur_year["duree_jour__sum"] + \
            somme_vols_nuit_cdb_cur_year["duree_nuit__sum"] + \
            somme_vols_jour_opl_cur_year["duree_jour__sum"] + \
            somme_vols_nuit_opl_cur_year["duree_nuit__sum"] + \
            somme_vols_jour_inst_cur_year["duree_jour__sum"] + \
            somme_vols_nuit_inst_cur_year["duree_nuit__sum"]

        liste_somme_vols_last_year = somme_vols_jour_cdb_last_year["duree_jour__sum"] + \
            somme_vols_nuit_cdb_last_year["duree_nuit__sum"] + \
            somme_vols_jour_opl_last_year["duree_jour__sum"] + \
            somme_vols_nuit_opl_last_year["duree_nuit__sum"] + \
            somme_vols_jour_inst_last_year["duree_jour__sum"] + \
            somme_vols_nuit_inst_last_year["duree_nuit__sum"]

        liste_somme_vols_total_total = somme_vols_jour_cdb_total["duree_jour__sum"] + \
            somme_vols_nuit_cdb_total["duree_nuit__sum"] + \
            somme_vols_jour_opl_total["duree_jour__sum"] + \
            somme_vols_nuit_opl_total["duree_nuit__sum"] + \
            somme_vols_jour_inst_total["duree_jour__sum"] + \
            somme_vols_nuit_inst_total["duree_nuit__sum"]

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
            somme_vols_arrivee_ifr_total,
        ])

    data = {
        'liste_somme_vols_cur_year': liste_somme_vols_cur_year,
        'liste_somme_vols_last_year': liste_somme_vols_last_year,
        'liste_somme_vols_total': liste_somme_vols_total,
    }

    return render(request, 'vol/somme.html', {'data': data})


def convert_timedelta_minutes_to_hours(duration):
    """ Convert a timedelta from format mm:ss to hh:mm """
    if duration != '':
        duration = duration * 60
    else:
        duration = timedelta(0)
    return duration


@login_required
def new_vol(request):
    """ Render the new flight page and save the new flight. """
    if request.method == "POST":
        # form_vol = VolForm(request.POST, current_user=request.user)
        form_vol = VolForm(request.POST)
        if form_vol.is_valid():
            vol = form_vol.save(commit=False)
            vol.duree_jour = convert_timedelta_minutes_to_hours(vol.duree_jour)
            vol.duree_nuit = convert_timedelta_minutes_to_hours(vol.duree_nuit)
            vol.duree_ifr = convert_timedelta_minutes_to_hours(vol.duree_ifr)
            vol.duree_simu = convert_timedelta_minutes_to_hours(vol.duree_simu)
            vol.duree_dc = convert_timedelta_minutes_to_hours(vol.duree_dc)
            vol.user_id = request.user
            vol.save()
            return redirect('index')
    else:
        # form_vol = VolForm(current_user=request.user)
        form_vol = VolForm()
    return render(request, 'vol/vol_add.html', {'form': form_vol})


def convert_timedelta(duration):
    if len(duration) < 8:
        duration = convert_empty_string_to_timedelta(duration)
    return duration


@login_required
def edit_vol(request, pk):
    """ Edit an existing flight via the new_vol view and save the edited flight. """
    current_user = request.user
    vols_list = Vol.objects.filter(user_id=current_user.id)
    vol = get_object_or_404(vols_list, pk=pk)
    if request.method == "POST":
        form = VolForm(request.POST, instance=vol)
        if current_user == vol.user_id:
            if form.is_valid():
                vol = form.save(commit=False)
                # print(vol.duree_jour)
                if form.has_changed():
                    print("Le champ suivant change : %s" % ", ".join(form.changed_data))
                # vol_duree_jour = Vol.objects.get(pk=pk)
                # print(vol_duree_jour.duree_jour)

                # vol.duree_jour = convert_timedelta_minutes_to_hours(vol.duree_jour)
                # vol.duree_nuit = convert_timedelta_minutes_to_hours(vol.duree_nuit)
                # vol.duree_simu = convert_timedelta_minutes_to_hours(vol.duree_simu)
                # vol.duree_ifr = convert_timedelta_minutes_to_hours(vol.duree_ifr)
                # vol.duree_dc = convert_timedelta_minutes_to_hours(vol.duree_dc)
                vol.save()
                return redirect('index')
    #    else:
    #       return render(request, 'vol/error_not_allowed.html')
    else:
        form = VolForm(instance=vol)
    return render(request, 'vol/vol_add.html', {'form': form})


@login_required
def remove_vol(request, pk):
    """ Remove a given flight """
    current_user = request.user
    vols_list = Vol.objects.filter(user_id=current_user.id)
    vol = get_object_or_404(vols_list, pk=pk)
    vol.delete()
    return redirect('index')


@method_decorator(login_required, name='dispatch')
class ImmatriculationCreate(CreateView):
    model = Immatriculation
    template_name = 'vol/immatriculation_add.html'
    fields = ['immatriculation',
              'type_avion']
    success_url = '/immatriculation_add'
    # template_name_suffix = '_add'

    def get_context_data(self, **kwargs):
        context = super(ImmatriculationCreate, self).get_context_data(**kwargs)
        immatriculation_list = Immatriculation.objects.order_by('immatriculation').filter(user_id=self.request.user)
        context['immatriculation_list'] = immatriculation_list
        return context

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super(ImmatriculationCreate, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@method_decorator(login_required, name='dispatch')
class ImmatriculationUpdate(UpdateView):
    model = Immatriculation
    template_name = 'vol/immatriculation_add.html'
    fields = ['immatriculation',
              'type_avion']
    success_url = '/immatriculation_add'
    # template_name_suffix = '_add'

    def get_context_data(self, **kwargs):
        context = super(ImmatriculationUpdate, self).get_context_data(**kwargs)
        immatriculation_list = Immatriculation.objects.order_by('immatriculation').filter(user_id=self.request.user)
        context['immatriculation_list'] = immatriculation_list
        return context

    def get_queryset(self):
        qs = super(ImmatriculationUpdate, self).get_queryset()
        return qs.filter(user_id=self.request.user.profile.user_id)

    def form_valid(self, form):
        return super(ImmatriculationUpdate, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@method_decorator(login_required, name='dispatch')
class ImmatriculationDelete(DeleteView):
    model = Immatriculation
    # template_name = 'vol/immatriculation_add.html'
    # success_url = reverse_lazy('new_immatriculation')
    # template_name_suffix = '_delete_form'

    def get_queryset(self):
        qs = super(ImmatriculationDelete, self).get_queryset()
        return qs.filter(user_id=self.request.user.profile.user_id)

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    success_url = reverse_lazy('new_immatriculation')


@method_decorator(login_required, name='dispatch')
class PiloteCreate(CreateView):
    model = Pilote
    template_name = 'vol/pilote_add.html'
    fields = ['nom',
              'prenom']
    success_url = '/pilote_add'
    # template_name_suffix = '_add'

    def get_context_data(self, **kwargs):
        context = super(PiloteCreate, self).get_context_data(**kwargs)
        pilotes_list = Pilote.objects.order_by('nom', 'prenom').filter(user_id=self.request.user)
        context['pilotes_list'] = pilotes_list
        return context

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super(PiloteCreate, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@method_decorator(login_required, name='dispatch')
class PiloteUpdate(UpdateView):
    model = Pilote
    template_name = 'vol/pilote_add.html'
    fields = ['nom',
              'prenom']
    success_url = '/pilote_add'
    # template_name_suffix = '_add'

    def get_context_data(self, **kwargs):
        context = super(PiloteUpdate, self).get_context_data(**kwargs)
        pilotes_list = Pilote.objects.order_by('nom', 'prenom').filter(user_id=self.request.user)
        context['pilotes_list'] = pilotes_list
        return context

    def get_queryset(self):
        qs = super(PiloteUpdate, self).get_queryset()
        return qs.filter(user_id=self.request.user.profile.user_id)

    def form_valid(self, form):
        # form.instance.user_id = self.request.user
        return super(PiloteUpdate, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@method_decorator(login_required, name='dispatch')
class PiloteDelete(DeleteView):
    model = Pilote
    # template_name = 'vol/pilote_add.html'
    # success_url = reverse_lazy('new_immatriculation')
    # template_name_suffix = '_delete_form'

    def get_queryset(self):
        qs = super(PiloteDelete, self).get_queryset()
        return qs.filter(user_id=self.request.user.profile.user_id)

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    success_url = reverse_lazy('new_pilote')


@method_decorator(login_required, name='dispatch')
class CodeIataCreate(CreateView):
    model = CodeIata
    template_name = 'vol/iata_add.html'
    fields = ['code_iata',
              'ville']
    success_url = '/iata_add'
    # template_name_suffix = '_add'

    def get_context_data(self, **kwargs):
        context = super(CodeIataCreate, self).get_context_data(**kwargs)
        iata_list = CodeIata.objects.order_by('code_iata').filter(user_id=self.request.user)
        context['iata_list'] = iata_list
        return context

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super(CodeIataCreate, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@method_decorator(login_required, name='dispatch')
class CodeIataUpdate(UpdateView):
    model = CodeIata
    template_name = 'vol/iata_add.html'
    fields = ['code_iata',
              'ville']
    success_url = '/iata_add'
    # template_name_suffix = '_add'

    def get_context_data(self, **kwargs):
        context = super(CodeIataUpdate, self).get_context_data(**kwargs)
        iata_list = CodeIata.objects.order_by('code_iata').filter(user_id=self.request.user)
        context['iata_list'] = iata_list
        return context

    def get_queryset(self):
        qs = super(CodeIataUpdate, self).get_queryset()
        return qs.filter(user_id=self.request.user.profile.user_id)

    def form_valid(self, form):
        # form.instance.user_id = self.request.user
        return super(CodeIataUpdate, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@method_decorator(login_required, name='dispatch')
class CodeIataDelete(DeleteView):
    model = CodeIata
    # template_name = 'vol/iata_add.html'
    # success_url = reverse_lazy('new_immatriculation')
    # template_name_suffix = '_delete_form'

    def get_queryset(self):
        qs = super(CodeIataDelete, self).get_queryset()
        return qs.filter(user_id=self.request.user.profile.user_id)

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    success_url = reverse_lazy('new_code_iata')


@method_decorator(login_required, name='dispatch')
class TypeAvionCreate(CreateView):
    model = TypeAvion
    template_name = 'vol/type_avion_add.html'
    fields = ['type_avion',
              'nb_moteurs']
    success_url = '/type_avion_add'
    # template_name_suffix = '_add'

    def get_context_data(self, **kwargs):
        context = super(TypeAvionCreate, self).get_context_data(**kwargs)
        type_avion_list = TypeAvion.objects.order_by('type_avion').filter(user_id=self.request.user)
        context['type_avion_list'] = type_avion_list
        return context

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super(TypeAvionCreate, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@method_decorator(login_required, name='dispatch')
class TypeAvionUpdate(UpdateView):
    model = TypeAvion
    template_name = 'vol/type_avion_add.html'
    fields = ['type_avion',
              'nb_moteurs']
    success_url = '/type_avion_add'
    # template_name_suffix = '_add'

    def get_context_data(self, **kwargs):
        context = super(TypeAvionUpdate, self).get_context_data(**kwargs)
        type_avion_list = TypeAvion.objects.order_by('type_avion').filter(user_id=self.request.user)
        context['type_avion_list'] = type_avion_list
        return context

    def get_queryset(self):
        qs = super(TypeAvionUpdate, self).get_queryset()
        return qs.filter(user_id=self.request.user.profile.user_id)

    def form_valid(self, form):
        # form.instance.user_id = self.request.user
        return super(TypeAvionUpdate, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@method_decorator(login_required, name='dispatch')
class TypeAvionDelete(DeleteView):
    model = TypeAvion
    # template_name = 'vol/iata_add.html'
    # success_url = reverse_lazy('new_immatriculation')
    # template_name_suffix = '_delete_form'

    def get_queryset(self):
        qs = super(TypeAvionDelete, self).get_queryset()
        return qs.filter(user_id=self.request.user.profile.user_id)

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    success_url = reverse_lazy('new_type_avion')
