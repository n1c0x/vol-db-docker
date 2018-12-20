from django.contrib import admin
from .models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from admin_totals.admin import ModelAdminTotals
from django.db.models import Sum, Avg
from django.db.models.functions import Coalesce


# Register your models here.



class VolResource(resources.ModelResource):
    class Meta:
        model = Vol
        fields = ('id','date','cdb','opl',)

class VolAdmin(ImportExportModelAdmin):
    resource_class = VolResource


class VolAdmin(ModelAdminTotals):
    fieldsets = [
        ('Date Information',          {'fields' : ['date']}),
        ('Personnel présent',         {'fields' : ['cdb','opl']}),
        ('Personnel supplémentaire',  {
            'classes' : ('collapse',),
            'fields' : ['obs1','obs2','instructeur']}),
        ('Code AITA des aéroports de départ et d\'arrivée',         {'fields' : ['depart','arrivee']}),
        ('Durée',         {'fields' : ['duree_jour','duree_nuit']}),
        ('Autre',          {'fields' : ['fonction','poste','immatriculation']}),
        ('Simulateur',          {
            'classes' : ('collapse',),
            'fields' : ['simu','duree_simu']}),
        ('IFR',          {
            'classes' : ('collapse',),
            'fields' : ['arrivee_ifr','duree_ifr_jour','duree_ifr_nuit']}),
        ('Observations',          {
            'classes' : ('collapse',),
            'fields' : ['observation']}),
    ]

    def fonction_description(self,object):
        return object.fonction
    fonction_description.short_description = "Fonction"
    def poste_description(self,object):
        return object.poste
    poste_description.short_description = "Poste"
    def get_type_avion(self, obj):
        return obj.immatriculation.type_avion
    get_type_avion.short_description = "Avion"

    list_display = ['date','depart','arrivee', 'duree_jour','duree_nuit','cdb','opl','get_type_avion']
    list_totals = [
        ('duree_jour', lambda field: Coalesce(Sum(field), 0)), ('duree_jour', Sum),
        ('duree_nuit', lambda field: Coalesce(Sum(field), 0)), ('duree_nuit', Sum),
    ]
    list_filter = ['date','arrivee_ifr']
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
        'immatriculation__type_avion__type_avion',
        ]


class CodeAitaAdmin(admin.ModelAdmin):
    list_display = ('code_aita','ville',)

class ImmatriculationAdmin(admin.ModelAdmin):
    list_display = ('immatriculation','type_avion',)
    list_filter = ['type_avion']

class TypeAvionAdmin(admin.ModelAdmin):
    list_display = ('type_avion','nb_moteurs',)
    list_filter = ['nb_moteurs']

class PiloteAdmin(admin.ModelAdmin):
    list_display = ('prenom','nom',)

admin.site.register(CodeAita,CodeAitaAdmin)
admin.site.register(TypeAvion,TypeAvionAdmin)
admin.site.register(Immatriculation,ImmatriculationAdmin)
admin.site.register(Pilote,PiloteAdmin)
admin.site.register(Vol,VolAdmin)

