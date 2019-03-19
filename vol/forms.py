from django import forms
from tempus_dominus.widgets import DatePicker
from .models import *
from .views import *


class VolForm(forms.ModelForm):
    """ Generate the flight form. """
    'ToDo : Set default value of cdp/opl according to the status of the pilot.'
    'If the pilot is a CDB, set the default value of cdb to "user.prenom user.nom". '
    'If the pilot is an OPL, set the default value of opl to "user.prenom user.nom". '

    def get_current_user(self):
        return self.current_user

    immatriculation = forms.ModelChoiceField(queryset=Immatriculation.objects.all(), label="Avion")
    # immatriculation = forms.ModelChoiceField(queryset=Immatriculation.objects.filter(user_id=get_current_user(""), label="Avion"))
    observation = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 4}))
    date = forms.DateField(widget=DatePicker(attrs={'autocomplete': 'off', }))
    duree_jour = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'HH:MM', 'maxlength': 5}), required=False)
    duree_nuit = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'HH:MM', }), required=False)
    duree_ifr = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'HH:MM', }), label="Durée IFR", required=False)
    duree_simu = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'HH:MM', }), required=False)
    duree_dc = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'HH:MM', }), required=False)
    vol_ifr = forms.ChoiceField(choices=Vol.ARRIVEE_IFR, label="Arrivées IFR", initial='1')

    class Meta:
        model = Vol
        fields = (
            'date',
            'cdb',
            'opl',
            'obs1',
            'obs2',
            'instructeur',
            'depart',
            'arrivee',
            'duree_jour',
            'duree_nuit',
            'fonction',
            'poste',
            'immatriculation',
            'observation',
            'vol_ifr',
            'duree_ifr',
            'vol_dc',
            'duree_dc',
            'vol_simu',
            'duree_simu',
            'user_id')
        exclude = ['user_id']


# class ImmatriculationForm(forms.ModelForm):
#     """ Generate the immatriculation form. """
#     class Meta:
#         model = Immatriculation
#         fields = (
#             'immatriculation',
#             'type_avion',
#             'user_id')
#         exclude = ['user_id']


class TypeAvionForm(forms.ModelForm):
    """ Generate the plane type form. """
    class Meta:
        model = TypeAvion
        fields = (
            'type_avion',
            'nb_moteurs',
            'user_id')
        exclude = ['user_id']


class PiloteForm(forms.ModelForm):
    """ Generate the pilot form. """
    class Meta:
        model = Pilote
        fields = (
            'prenom',
            'nom',
            'user_id')
        exclude = ['user_id']


class IataForm(forms.ModelForm):
    """ Generate the IATA code form. """
    class Meta:
        model = CodeIata
        fields = (
            'code_iata',
            'ville',
            'user_id')
        exclude = ['user_id']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('client_type', 'current_position', 'employer')
