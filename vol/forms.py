from django import forms


from .models import *


class VolForm(forms.ModelForm):
    'ToDo : Set default value of cdp/opl according to the status of the pilot.'
    'If the pilot is a CDB, set the default value of cdb to "user.prenom user.nom". '
    'If the pilot is an OPL, set the default value of opl to "user.prenom user.nom". '

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


class ImmatriculationForm(forms.ModelForm):
    class Meta:
        model = Immatriculation
        fields = (
            'immatriculation',
            'type_avion',
            'user_id')
        exclude = ['user_id']


class TypeAvion(forms.ModelForm):
    class Meta:
        model = TypeAvion
        fields = (
            'type_avion',
            'nb_moteurs',
            'user_id')
        exclude = ['user_id']


class PiloteForm(forms.ModelForm):
    class Meta:
        model = Pilote
        fields = (
            'prenom',
            'nom',
            'user_id')
        exclude = ['user_id']
