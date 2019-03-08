from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from admin_totals.admin import ModelAdminTotals
from django.db.models import Sum
from django.db.models.functions import Coalesce


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Client'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


class VolAdmin(ModelAdminTotals):
    fieldsets = [
        ('Date Information', {'fields': ['date']}),
        ('Personnel présent', {'fields': ['cdb', 'opl']}),
        ('Personnel supplémentaire', {'classes': ('collapse',),
                                      'fields': ['obs1', 'obs2', 'instructeur']}),
        ('Code IATA des aéroports de départ et d\'arrivée', {'fields': ['depart', 'arrivee']}),
        ('Durée', {'fields': ['duree_jour', 'duree_nuit']}),
        ('Autre', {'fields': ['fonction', 'poste', 'immatriculation']}),
        ('Simulateur', {
            'classes': ('collapse',),
            'fields': ['vol_simu', 'duree_simu']}),
        ('IFR', {
            'classes': ('collapse',),
            'fields': ['vol_ifr', 'duree_ifr']}),
        ('Doubles commandes', {
            'classes': ('collapse',),
            'fields': ['vol_dc', 'duree_dc']}),
        ('Observations', {
            'classes': ('collapse',),
            'fields': ['observation']}),
        ('Utilisateur', {'fields': ['user_id']}),
    ]

    def fonction_description(self, obj):
        return obj.fonction
    fonction_description.short_description = "Fonction"

    def poste_description(self, obj):
        return obj.poste
    poste_description.short_description = "Poste"

    def get_type_avion(self, obj):
        return obj.immatriculation.type_avion
    get_type_avion.short_description = "Avion"

    def total_general_count(self, obj):
        if obj.duree_jour and obj.duree_nuit:
            return obj.duree_jour + obj.duree_nuit
    total_general_count.short_description = "Total Jour + Nuit"

    def total_vol_ifr(self, obj):
        return obj.vol_ifr.annotate(filter(vol_fr=True))

    def vol_dc_description(self, obj):
        return obj.vol_dc
    vol_dc_description.short_description = "Vol DC"

    list_display = ['date',
                    'depart',
                    'arrivee',
                    'duree_jour',
                    'duree_nuit',
                    'total_general_count',
                    'duree_ifr',
                    'vol_ifr',
                    'vol_dc',
                    'duree_dc',
                    'vol_simu',
                    'duree_simu',
                    'cdb',
                    'opl',
                    'get_type_avion',
                    'poste',
                    'user_id']
    list_totals = [
        ('duree_jour', lambda field: Coalesce(Sum(field), 0)), ('duree_jour', Sum),
        ('duree_nuit', lambda field: Coalesce(Sum(field), 0)), ('duree_nuit', Sum),
        ('duree_ifr', lambda field: Coalesce(Sum(field), 0)), ('duree_ifr', Sum),
        ('duree_simu', lambda field: Coalesce(Sum(field), 0)), ('duree_simu', Sum),
        ('duree_dc', lambda field: Coalesce(Sum(field), 0)), ('duree_dc', Sum),
        ('vol_ifr', lambda field: Coalesce(Sum(field), 0)), ('total_vol_ifr', Sum),
    ]
    list_filter = ['date', 'immatriculation__type_avion__type_avion', 'poste', 'vol_ifr', 'vol_simu', 'vol_dc']
    search_fields = [
        'cdb__prenom',
        'cdb__nom',
        'opl__prenom',
        'opl__nom',
        'obs1__prenom',
        'obs1__nom',
        'obs2__prenom',
        'obs2__nom',
        'instructeur__prenom',
        'instructeur__nom',
        'immatriculation__type_avion__type_avion']


class CodeIataAdmin(admin.ModelAdmin):
    list_display = ('code_iata', 'ville', 'user_id')


class ImmatriculationAdmin(admin.ModelAdmin):
    list_display = ('immatriculation', 'type_avion', 'user_id')
    list_filter = ['type_avion']


class TypeAvionAdmin(admin.ModelAdmin):
    list_display = ('type_avion', 'nb_moteurs', 'user_id')
    list_filter = ['nb_moteurs']


class PiloteAdmin(admin.ModelAdmin):
    list_display = ('prenom', 'nom', 'user_id')


admin.site.register(CodeIata, CodeIataAdmin)
admin.site.register(TypeAvion, TypeAvionAdmin)
admin.site.register(Immatriculation, ImmatriculationAdmin)
admin.site.register(Pilote, PiloteAdmin)
admin.site.register(Vol, VolAdmin)
# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
