from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, ProtectedError, Q, Count
from django.db import IntegrityError
from .forms import VolForm, ImmatriculationForm, UserForm, ProfileForm
from django.shortcuts import redirect, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import date, datetime, timedelta
from .models import *
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator


def handler400(request, template_name="400.html"):
    response = render_to_response("errors/400.html")
    response.status_code = 400
    return response


def handler403(request, template_name="403.html"):
    response = render_to_response("errors/403.html")
    response.status_code = 403
    return response


def handler404(request, exception, template_name="404.html"):
    response = render_to_response("errors/404.html")
    response.status_code = 404
    return response


def handler500(request, template_name="500.html"):
    response = render_to_response("errors/500.html")
    response.status_code = 500
    return response


@login_required
def index(request):
    """
    Render the home page.

    **Template:**

    :template:`vol/index.html`

    """
    current_user = request.user
    data = {}

    count_pilots = Pilote.objects.filter(user_id=current_user.id).count()
    count_airports = CodeIata.objects.filter(user_id=current_user.id).count()
    count_planes = Immatriculation.objects.filter(user_id=current_user.id).count()
    last_flight = Vol.objects.filter(user_id=current_user.id).latest('date')
    last_flight_total_duration = last_flight.duree_jour + last_flight.duree_nuit
    top_src_dest = Vol.objects.filter(user_id=current_user.id).values('depart__code_iata', 'arrivee__code_iata').annotate(src_dest_count=Count('*')).order_by('-src_dest_count')
    top_airport_from = Vol.objects.filter(user_id=current_user.id).values('depart__code_iata', 'depart__ville').annotate(airport_count=Count('*')).order_by('-airport_count')
    top_airport_to = Vol.objects.filter(user_id=current_user.id).values('arrivee__code_iata', 'arrivee__ville').annotate(airport_count=Count('*')).order_by('-airport_count')
    top_plane = Vol.objects.filter(user_id=current_user.id).values('immatriculation__immatriculation', 'immatriculation__type_avion__type_avion').annotate(plane_count=Count('*')).order_by('-plane_count')
    top_pilot_cdb = Vol.objects.filter(user_id=current_user.id).values('cdb__prenom', 'cdb__nom').annotate(pilot_count=Count('*')).order_by('-pilot_count')

    data['count_pilots'] = count_pilots
    data['count_airports'] = count_airports
    data['count_planes'] = count_planes
    data['last_flight'] = last_flight
    data['last_flight_total_duration'] = last_flight_total_duration
    data['top_src_dest'] = top_src_dest
    data['top_airport_from'] = top_airport_from
    data['top_airport_to'] = top_airport_to
    data['top_plane'] = top_plane
    data['top_pilot_cdb'] = top_pilot_cdb

    return render(request, 'vol/index.html', {'data': data})


@login_required
def get_user_profile(request, username):
    """ Render the current user profile on the profile page. """
    user = User.objects.get(username=username)
    return render(request, 'vol/profile.html', {"user": user})


@login_required
def update_user_profile(request, username):
    """ Update the user profile """
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
    """
        Class which lists all the flights
    """
    model = Vol
    template_name = 'vol/flight_list.html'

    def get_queryset(self):
        """ Override the standard get_query method. The override orders by date and filters by current user """
        return Vol.objects.order_by('-date').filter(user_id=self.request.user)

    def dispatch(self, *args, **kwargs):
        """ Forces a login to view this page """
        return super().dispatch(*args, **kwargs)


@method_decorator(login_required, name='dispatch')
class VolDetail(DetailView):
    """ Class which displays the details of a given flight """
    model = Vol
    template_name = 'vol/detail.html'
    # vol = Vol.objects.filter(user_id=self.request.user)

    def get_context_data(self, **kwargs):
        """ Override the standard get_context_data. The override filters by current user """
        context = super(VolDetail, self).get_context_data(**kwargs)
        vols_list = Vol.objects.filter(user_id=self.request.user)
        vol = get_object_or_404(vols_list, pk=self.kwargs.get('pk', None))
        context['vol'] = vol
        return context

    def dispatch(self, *args, **kwargs):
        """ Forces a login to view this page """
        return super().dispatch(*args, **kwargs)


@login_required
def somme(request):
    """
        Render the sum page. This page displays the sums of all the flights
        grouped by plane type, year and function.
    """
    current_user = request.user
    avions = TypeAvion.objects.filter(user_id=current_user.id)

    liste_somme_vols_cur_year = []
    liste_somme_vols_last_year = []
    dict_somme_vols_total = {}
    liste_somme_vols_total_total = []

    for modele_avion in avions:

        today = date.today()
        current_year = datetime(today.year, 1, 1)

        # Current Year
        somme_vols_jour_cdb_cur_year = Vol.objects.filter(
            poste="PIC",
            immatriculation__type_avion__type_avion=modele_avion,
            date__year=current_year.year,
            user_id=current_user.id).aggregate(Sum('duree_jour'))
        somme_vols_nuit_cdb_cur_year = Vol.objects.filter(
            poste="PIC",
            immatriculation__type_avion__type_avion=modele_avion,
            date__year=current_year.year,
            user_id=current_user.id).aggregate(Sum('duree_nuit'))
        somme_vols_jour_opl_cur_year = Vol.objects.filter(
            poste="FO",
            immatriculation__type_avion__type_avion=modele_avion,
            date__year=current_year.year,
            user_id=current_user.id).aggregate(Sum('duree_jour'))
        somme_vols_nuit_opl_cur_year = Vol.objects.filter(
            poste="FO",
            immatriculation__type_avion__type_avion=modele_avion,
            date__year=current_year.year,
            user_id=current_user.id).aggregate(Sum('duree_nuit'))
        somme_vols_jour_inst_cur_year = Vol.objects.filter(
            poste="INSTRUCT",
            immatriculation__type_avion__type_avion=modele_avion,
            date__year=current_year.year,
            user_id=current_user.id).aggregate(Sum('duree_jour'))
        somme_vols_nuit_inst_cur_year = Vol.objects.filter(
            poste="INSTRUCT",
            immatriculation__type_avion__type_avion=modele_avion,
            date__year=current_year.year,
            user_id=current_user.id).aggregate(Sum('duree_nuit'))
        somme_vols_simu_cur_year = Vol.objects.filter(
            immatriculation__type_avion__type_avion=modele_avion,
            date__year=current_year.year,
            user_id=current_user.id).aggregate(Sum('duree_simu'))
        somme_vols_ifr_cur_year = Vol.objects.filter(
            immatriculation__type_avion__type_avion=modele_avion,
            date__year=current_year.year,
            user_id=current_user.id).aggregate(Sum('duree_ifr'))
        somme_vols_arrivee_ifr_cur_year = Vol.objects.filter(
            immatriculation__type_avion__type_avion=modele_avion,
            date__year=current_year.year,
            user_id=current_user.id,
            vol_ifr__gt=0).aggregate(Sum('vol_ifr'))
        somme_vols_jour_dc_cur_year = []
        somme_vols_nuit_dc_cur_year = []

        # Last Year
        somme_vols_jour_cdb_last_year = Vol.objects.filter(
            poste="PIC",
            immatriculation__type_avion__type_avion=modele_avion,
            user_id=current_user.id).exclude(date__gt=current_year).aggregate(Sum('duree_jour'))
        somme_vols_nuit_cdb_last_year = Vol.objects.filter(
            poste="PIC",
            immatriculation__type_avion__type_avion=modele_avion,
            user_id=current_user.id).exclude(date__gt=current_year).aggregate(Sum('duree_nuit'))
        somme_vols_jour_opl_last_year = Vol.objects.filter(
            poste="FO",
            immatriculation__type_avion__type_avion=modele_avion,
            user_id=current_user.id).exclude(date__gt=current_year).aggregate(Sum('duree_jour'))
        somme_vols_nuit_opl_last_year = Vol.objects.filter(
            poste="FO",
            immatriculation__type_avion__type_avion=modele_avion,
            user_id=current_user.id).exclude(date__gt=current_year).aggregate(Sum('duree_nuit'))
        somme_vols_jour_inst_last_year = Vol.objects.filter(
            poste="INSTRUCT",
            immatriculation__type_avion__type_avion=modele_avion,
            user_id=current_user.id).exclude(date__gt=current_year).aggregate(Sum('duree_jour'))
        somme_vols_nuit_inst_last_year = Vol.objects.filter(
            poste="INSTRUCT",
            immatriculation__type_avion__type_avion=modele_avion,
            user_id=current_user.id).exclude(date__gt=current_year).aggregate(Sum('duree_nuit'))
        somme_vols_simu_last_year = Vol.objects.filter(
            immatriculation__type_avion__type_avion=modele_avion,
            user_id=current_user.id).exclude(date__gt=current_year).aggregate(Sum('duree_simu'))
        somme_vols_ifr_last_year = Vol.objects.filter(
            immatriculation__type_avion__type_avion=modele_avion,
            user_id=current_user.id).exclude(date__gt=current_year).aggregate(Sum('duree_ifr'))
        somme_vols_arrivee_ifr_last_year = Vol.objects.filter(
            immatriculation__type_avion__type_avion=modele_avion,
            user_id=current_user.id,
            vol_ifr__gt=0).exclude(date__gt=current_year).aggregate(Sum('vol_ifr'))
        somme_vols_jour_dc_last_year = []
        somme_vols_nuit_dc_last_year = []

        # Total Year
        somme_vols_jour_cdb_total = Vol.objects.filter(
            poste="PIC",
            immatriculation__type_avion__type_avion=modele_avion,
            user_id=current_user.id).aggregate(Sum('duree_jour'))
        somme_vols_nuit_cdb_total = Vol.objects.filter(
            poste="PIC",
            immatriculation__type_avion__type_avion=modele_avion,
            user_id=current_user.id).aggregate(Sum('duree_nuit'))
        somme_vols_jour_opl_total = Vol.objects.filter(
            poste="FO",
            immatriculation__type_avion__type_avion=modele_avion,
            user_id=current_user.id).aggregate(Sum('duree_jour'))
        somme_vols_nuit_opl_total = Vol.objects.filter(
            poste="FO",
            immatriculation__type_avion__type_avion=modele_avion,
            user_id=current_user.id).aggregate(Sum('duree_nuit'))
        somme_vols_jour_inst_total = Vol.objects.filter(
            poste="INSTRUCT",
            immatriculation__type_avion__type_avion=modele_avion,
            user_id=current_user.id).aggregate(Sum('duree_jour'))
        somme_vols_nuit_inst_total = Vol.objects.filter(
            poste="INSTRUCT",
            immatriculation__type_avion__type_avion=modele_avion,
            user_id=current_user.id).aggregate(Sum('duree_nuit'))
        somme_vols_simu_total = Vol.objects.filter(
            immatriculation__type_avion__type_avion=modele_avion,
            user_id=current_user.id).aggregate(Sum('duree_simu'))
        somme_vols_ifr_total = Vol.objects.filter(
            immatriculation__type_avion__type_avion=modele_avion,
            user_id=current_user.id).aggregate(Sum('duree_ifr'))
        somme_vols_arrivee_ifr_total = Vol.objects.filter(
            immatriculation__type_avion__type_avion=modele_avion,
            user_id=current_user.id,
            vol_ifr__gt=0).aggregate(Sum('vol_ifr'))
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
        if somme_vols_ifr_cur_year["duree_ifr__sum"] is None:
            somme_vols_ifr_cur_year["duree_ifr__sum"] = timedelta(0)

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
        if somme_vols_ifr_last_year["duree_ifr__sum"] is None:
            somme_vols_ifr_last_year["duree_ifr__sum"] = timedelta(0)

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
        if somme_vols_simu_total["duree_simu__sum"] is None:
            somme_vols_simu_total["duree_simu__sum"] = timedelta(0)
        if somme_vols_ifr_total["duree_ifr__sum"] is None:
            somme_vols_ifr_total["duree_ifr__sum"] = timedelta(0)

        # Total de tous les vols
        liste_somme_vols_cur_year = somme_vols_jour_cdb_cur_year["duree_jour__sum"] + \
            somme_vols_nuit_cdb_cur_year["duree_nuit__sum"] + \
            somme_vols_jour_opl_cur_year["duree_jour__sum"] + \
            somme_vols_nuit_opl_cur_year["duree_nuit__sum"] + \
            somme_vols_jour_inst_cur_year["duree_jour__sum"] + \
            somme_vols_nuit_inst_cur_year["duree_nuit__sum"] + \
            somme_vols_simu_cur_year["duree_simu__sum"] + \
            somme_vols_ifr_cur_year["duree_ifr__sum"]
        # Ne pas oublier de rajouter DC

        liste_somme_vols_last_year = somme_vols_jour_cdb_last_year["duree_jour__sum"] + \
            somme_vols_nuit_cdb_last_year["duree_nuit__sum"] + \
            somme_vols_jour_opl_last_year["duree_jour__sum"] + \
            somme_vols_nuit_opl_last_year["duree_nuit__sum"] + \
            somme_vols_jour_inst_last_year["duree_jour__sum"] + \
            somme_vols_nuit_inst_last_year["duree_nuit__sum"] + \
            somme_vols_simu_last_year["duree_simu__sum"] + \
            somme_vols_ifr_last_year["duree_ifr__sum"]
        # Ne pas oublier de rajouter DC

        liste_somme_vols_total_total = somme_vols_jour_cdb_total["duree_jour__sum"] + \
            somme_vols_nuit_cdb_total["duree_nuit__sum"] + \
            somme_vols_jour_opl_total["duree_jour__sum"] + \
            somme_vols_nuit_opl_total["duree_nuit__sum"] + \
            somme_vols_jour_inst_total["duree_jour__sum"] + \
            somme_vols_nuit_inst_total["duree_nuit__sum"] + \
            somme_vols_simu_total["duree_simu__sum"] + \
            somme_vols_ifr_total["duree_ifr__sum"]
        # Ne pas oublier de rajouter DC

        dict_somme_vols_total[modele_avion] = {
            'somme_vols_jour_cdb_cur_year': somme_vols_jour_cdb_cur_year,
            'somme_vols_nuit_cdb_cur_year': somme_vols_nuit_cdb_cur_year,
            'somme_vols_jour_opl_cur_year': somme_vols_jour_opl_cur_year,
            'somme_vols_nuit_opl_cur_year': somme_vols_nuit_opl_cur_year,
            'somme_vols_jour_dc_cur_year': somme_vols_jour_dc_cur_year,
            'somme_vols_nuit_dc_cur_year': somme_vols_nuit_dc_cur_year,
            'somme_vols_jour_inst_cur_year': somme_vols_jour_inst_cur_year,
            'somme_vols_nuit_inst_cur_year': somme_vols_nuit_inst_cur_year,
            'somme_vols_simu_cur_year': somme_vols_simu_cur_year,
            'somme_vols_ifr_cur_year': somme_vols_ifr_cur_year,
            'somme_vols_arrivee_ifr_cur_year': somme_vols_arrivee_ifr_cur_year,
            'somme_vols_jour_cdb_last_year': somme_vols_jour_cdb_last_year,
            'somme_vols_nuit_cdb_last_year': somme_vols_nuit_cdb_last_year,
            'somme_vols_jour_opl_last_year': somme_vols_jour_opl_last_year,
            'somme_vols_nuit_opl_last_year': somme_vols_nuit_opl_last_year,
            'somme_vols_jour_dc_last_year': somme_vols_jour_dc_last_year,
            'somme_vols_nuit_dc_last_year': somme_vols_nuit_dc_last_year,
            'somme_vols_jour_inst_last_year': somme_vols_jour_inst_last_year,
            'somme_vols_nuit_inst_last_year': somme_vols_nuit_inst_last_year,
            'somme_vols_simu_last_year': somme_vols_simu_last_year,
            'somme_vols_ifr_last_year': somme_vols_ifr_last_year,
            'somme_vols_arrivee_ifr_last_year': somme_vols_arrivee_ifr_last_year,
            'somme_vols_jour_cdb_total': somme_vols_jour_cdb_total,
            'somme_vols_nuit_cdb_total': somme_vols_nuit_cdb_total,
            'somme_vols_jour_opl_total': somme_vols_jour_opl_total,
            'somme_vols_nuit_opl_total': somme_vols_nuit_opl_total,
            'somme_vols_jour_dc_total': somme_vols_jour_dc_total,
            'somme_vols_nuit_dc_total': somme_vols_nuit_dc_total,
            'somme_vols_jour_inst_total': somme_vols_jour_inst_total,
            'somme_vols_nuit_inst_total': somme_vols_nuit_inst_total,
            'somme_vols_ifr_total': somme_vols_ifr_total,
            'somme_vols_arrivee_ifr_total': somme_vols_arrivee_ifr_total,
            'liste_somme_vols_cur_year': convert_timedelta_days_to_seconds(liste_somme_vols_cur_year),
            'liste_somme_vols_last_year': convert_timedelta_days_to_seconds(liste_somme_vols_last_year),
            'liste_somme_vols_total_total': convert_timedelta_days_to_seconds(liste_somme_vols_total_total), }

    current_page = "total"

    return render(request, 'vol/somme.html', {'dict_somme_vols_total': dict_somme_vols_total})


def convert_timedelta_days_to_seconds(duration):
    d = duration.days
    s = duration.seconds + (d * 24 * 3600)
    h = s // 3600
    s = s - (h * 3600)
    m = s // 60
    s = s - (m * 60)
    return '{:02}:{:02}:{:02}'.format(int(h), int(m), int(s))


def convert_timedelta_minutes_to_hours(duration):
    """ Convert a timedelta from format mm:ss to hh:mm """
    # if duration != '':
    #     duration = duration * 60
    if duration == '':
        duration = timedelta(0)
    return duration


@method_decorator(login_required, name='dispatch')
class VolCreate(CreateView):
    """ Class to create a flight """
    model = Vol
    template_name = 'vol/vol_add.html'
    form_class = VolForm
    success_url = '/vols'
    # template_name_suffix = '_add'

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs['user_id'] = self.request.user.id
        return kwargs

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        form.instance.duree_jour = convert_timedelta_minutes_to_hours(form.instance.duree_jour)
        form.instance.duree_nuit = convert_timedelta_minutes_to_hours(form.instance.duree_nuit)
        form.instance.duree_ifr = convert_timedelta_minutes_to_hours(form.instance.duree_ifr)
        form.instance.duree_simu = convert_timedelta_minutes_to_hours(form.instance.duree_simu)
        form.instance.duree_dc = convert_timedelta_minutes_to_hours(form.instance.duree_dc)
        return super(VolCreate, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        """ Forces a login to view this page """
        return super().dispatch(*args, **kwargs)


def convert_timedelta(duration):
    if len(duration) < 8:
        duration = convert_empty_string_to_timedelta(duration)
    return duration


@method_decorator(login_required, name='dispatch')
class VolUpdate(UpdateView):
    """ Class to update a flight """
    model = Vol
    template_name = 'vol/vol_add.html'
    form_class = VolForm
    success_url = '/vols'
    # template_name_suffix = '_add'

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs['user_id'] = self.request.user.id
        return kwargs

    def form_valid(self, form):
        if form.has_changed():
            print("Le champ suivant change : %s" % ", ".join(form.changed_data))
        # vol_duree_jour = Vol.objects.get(pk=pk)
        # print(vol_duree_jour.duree_jour)
        # form.instance.duree_jour = convert_timedelta_minutes_to_hours(form.instance.duree_jour)
        # form.instance.duree_nuit = convert_timedelta_minutes_to_hours(form.instance.duree_nuit)
        # form.instance.duree_ifr = convert_timedelta_minutes_to_hours(form.instance.duree_simu)
        # form.instance.duree_simu = convert_timedelta_minutes_to_hours(form.instance.duree_ifr)
        # form.instance.duree_dc = convert_timedelta_minutes_to_hours(form.instance.duree_dc)
        return super(VolUpdate, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        """ Forces a login to view this page """
        return super().dispatch(*args, **kwargs)


@method_decorator(login_required, name='dispatch')
class VolDelete(DeleteView):
    """ Class to delete a flight """
    model = Vol
    # template_name = 'vol/immatriculation_add.html'

    def get_queryset(self):
        qs = super(VolDelete, self).get_queryset()
        return qs.filter(user_id=self.request.user.profile.user_id)

    def dispatch(self, *args, **kwargs):
        """ Forces a login to view this page """
        return super().dispatch(*args, **kwargs)

    success_url = reverse_lazy('flight_list')


@method_decorator(login_required, name='dispatch')
class ImmatriculationCreate(CreateView):
    """ Class to create a plane """
    model = Immatriculation
    template_name = 'vol/immatriculation_add.html'
    form_class = ImmatriculationForm
    success_url = '/immatriculation_add'
    # template_name_suffix = '_add'

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs['user_id'] = self.request.user.id
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ImmatriculationCreate, self).get_context_data(**kwargs)
        immatriculation_list = Immatriculation.objects.order_by('immatriculation').filter(user_id=self.request.user)
        context['immatriculation_list'] = immatriculation_list
        context["immat_exists"] = []
        for immatriculation in immatriculation_list:
            entry = Vol.objects.filter(immatriculation=immatriculation.id)
            if entry.exists():
                context["immat_exists"].append((immatriculation.immatriculation, True),)
            else:
                context["immat_exists"].append((immatriculation.immatriculation, False),)
        return context

    def get_form(self, *args, **kwargs):
        form = super(ImmatriculationCreate, self).get_form(*args, **kwargs)
        form.fields['immatriculation'].queryset = Immatriculation.objects.filter(user_id=self.request.user)
        return form

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        try:
            return super(ImmatriculationCreate, self).form_valid(form)
        except IntegrityError:
            verbose_name_demonstrative = "cette " + Immatriculation._meta.verbose_name.title()
            verbose_name_plural = Immatriculation._meta.verbose_name_plural.title()
            data = {'verbose_name_demonstrative': verbose_name_demonstrative, 'verbose_name_plural': verbose_name_plural}
            return render_to_response('vol/integrity.html', {'data': data})

    def dispatch(self, *args, **kwargs):
        """ Forces a login to view this page """
        return super().dispatch(*args, **kwargs)


@method_decorator(login_required, name='dispatch')
class ImmatriculationUpdate(UpdateView):
    """ Class to update a plane """
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
        try:
            return super(ImmatriculationUpdate, self).form_valid(form)
        except IntegrityError:
            verbose_name_demonstrative = "cette " + Immatriculation._meta.verbose_name.title()
            verbose_name_plural = Immatriculation._meta.verbose_name_plural.title()
            data = {'verbose_name_demonstrative': verbose_name_demonstrative, 'verbose_name_plural': verbose_name_plural}
            return render_to_response('vol/integrity.html', {'data': data})

    def dispatch(self, *args, **kwargs):
        """ Forces a login to view this page """
        return super().dispatch(*args, **kwargs)


@method_decorator(login_required, name='dispatch')
class ImmatriculationDelete(DeleteView):
    """ Class to delete a plane """
    model = Immatriculation
    # template_name = 'vol/immatriculation_add.html'

    def get_queryset(self):
        qs = super(ImmatriculationDelete, self).get_queryset()
        return qs.filter(user_id=self.request.user.profile.user_id)

    def dispatch(self, *args, **kwargs):
        """ Forces a login to view this page """
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            # render the template with your message in the context
            # or you can use the messages framework to send the message
            previous_url = self.request.META.get('HTTP_REFERER')
            return render(request, 'vol/protect.html', {'previous_url': previous_url})

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
        pilots_list = Pilote.objects.order_by('nom', 'prenom').filter(user_id=self.request.user)
        context['pilots_list'] = pilots_list
        context["pilot_exists"] = []
        for pilot in pilots_list:
            entry = Vol.objects.filter(Q(cdb=pilot.id) | Q(opl=pilot.id) | Q(obs1=pilot.id) | Q(obs2=pilot.id) | Q(instructeur=pilot.id))
            if entry.exists():
                context["pilot_exists"].append((str(pilot), True),)
            else:
                context["pilot_exists"].append((str(pilot), False),)
        return context

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        try:
            return super(PiloteCreate, self).form_valid(form)
        except IntegrityError:
            verbose_name_demonstrative = "ce " + Pilote._meta.verbose_name.title()
            verbose_name_plural = Pilote._meta.verbose_name_plural.title()
            data = {'verbose_name_demonstrative': verbose_name_demonstrative, 'verbose_name_plural': verbose_name_plural}
            return render_to_response('vol/integrity.html', {'data': data})

    def dispatch(self, *args, **kwargs):
        """ Forces a login to view this page """
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
        pilots_list = Pilote.objects.order_by('nom', 'prenom').filter(user_id=self.request.user)
        context['pilots_list'] = pilots_list
        return context

    def get_queryset(self):
        qs = super(PiloteUpdate, self).get_queryset()
        return qs.filter(user_id=self.request.user.profile.user_id)

    def form_valid(self, form):
        # form.instance.user_id = self.request.user
        try:
            return super(PiloteUpdate, self).form_valid(form)
        except IntegrityError:
            verbose_name_demonstrative = "ce " + Pilote._meta.verbose_name.title()
            verbose_name_plural = Pilote._meta.verbose_name_plural.title()
            data = {'verbose_name_demonstrative': verbose_name_demonstrative, 'verbose_name_plural': verbose_name_plural}
            return render_to_response('vol/integrity.html', {'data': data})

    def dispatch(self, *args, **kwargs):
        """ Forces a login to view this page """
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
        """ Forces a login to view this page """
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            # render the template with your message in the context
            # or you can use the messages framework to send the message
            previous_url = self.request.META.get('HTTP_REFERER')
            return render(request, 'vol/protect.html', {'previous_url': previous_url})

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
        context["iata_exists"] = []
        for iata in iata_list:
            entry = Vol.objects.filter(Q(depart=iata.id) | Q(arrivee=iata.id))
            if entry.exists():
                context["iata_exists"].append((str(iata), True),)
            else:
                context["iata_exists"].append((str(iata), False),)
        return context

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        try:
            return super(CodeIataCreate, self).form_valid(form)
        except IntegrityError:
            verbose_name_demonstrative = "ce " + CodeIta._meta.verbose_name.title()
            verbose_name_plural = CodeIta._meta.verbose_name_plural.title()
            data = {'verbose_name_demonstrative': verbose_name_demonstrative, 'verbose_name_plural': verbose_name_plural}
            return render_to_response('vol/integrity.html', {'data': data})

    def dispatch(self, *args, **kwargs):
        """ Forces a login to view this page """
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
        try:
            return super(CodeIataUpdate, self).form_valid(form)
        except IntegrityError:
            verbose_name_demonstrative = "ce " + CodeIta._meta.verbose_name.title()
            verbose_name_plural = CodeIta._meta.verbose_name_plural.title()
            data = {'verbose_name_demonstrative': verbose_name_demonstrative, 'verbose_name_plural': verbose_name_plural}
            return render_to_response('vol/integrity.html', {'data': data})

    def dispatch(self, *args, **kwargs):
        """ Forces a login to view this page """
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
        """ Forces a login to view this page """
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            # render the template with your message in the context
            # or you can use the messages framework to send the message
            previous_url = self.request.META.get('HTTP_REFERER')
            return render(request, 'vol/protect.html', {'previous_url': previous_url})

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
        context["type_avion_exists"] = []
        for type_avion in type_avion_list:
            entry = Immatriculation.objects.filter(Q(type_avion=type_avion.id))
            if entry.exists():
                context["type_avion_exists"].append((str(type_avion), True),)
            else:
                context["type_avion_exists"].append((str(type_avion), False),)
        return context

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        try:
            return super(TypeAvionCreate, self).form_valid(form)
        except IntegrityError:
            verbose_name_demonstrative = "cette " + TypeAvion._meta.verbose_name.title()
            verbose_name_plural = TypeAvion._meta.verbose_name_plural.title()
            data = {'verbose_name_demonstrative': verbose_name_demonstrative, 'verbose_name_plural': verbose_name_plural}
            return render_to_response('vol/integrity.html', {'data': data})

    def dispatch(self, *args, **kwargs):
        """ Forces a login to view this page """
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
        try:
            return super(TypeAvionUpdate, self).form_valid(form)
        except IntegrityError:
            verbose_name_demonstrative = "cette " + TypeAvion._meta.verbose_name.title()
            verbose_name_plural = TypeAvion._meta.verbose_name_plural.title()
            data = {'verbose_name_demonstrative': verbose_name_demonstrative, 'verbose_name_plural': verbose_name_plural}
            return render_to_response('vol/integrity.html', {'data': data})

    def dispatch(self, *args, **kwargs):
        """ Forces a login to view this page """
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
        """ Forces a login to view this page """
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            # render the template with your message in the context
            # or you can use the messages framework to send the message
            previous_url = self.request.META.get('HTTP_REFERER')
            return render(request, 'vol/protect.html', {'previous_url': previous_url})

    success_url = reverse_lazy('new_type_avion')
