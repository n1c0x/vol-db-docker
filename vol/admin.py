from django.contrib import admin
from .models import *

# Register your models here.

class VolAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Date Information',          {'fields' : ['date']}),
        ('Personnel présent',         {'fields' : ['cdb','opl']}),
        ('Personnel supplémentaire',  {
            'classes' : ('collapse',),
            'fields' : ['obs1','obs2','instructeur']}),
        ('Code AITA des aéroports de départ et d\'arrivée',         {'fields' : ['depart','arrivee']}),
        ('Durée',         {'fields' : ['duree_jour','duree_nuit']}),
        ('Autre',          {'fields' : ['arrivee_ifr','simu','fonction','poste','immatriculation']}),
        ('Observations',          {
            'classes' : ('collapse',),
            'fields' : ['observation']}),
    ]
    list_display = ('date','depart','arrivee',)
    list_filter = ['date']
    save_as=True

class CodeAitaAdmin(admin.ModelAdmin):
    list_display = ('code_aita','ville',)

class ImmatriculationAdmin(admin.ModelAdmin):
    list_display = ('immatriculation','type_avion',)

class TypeAvionAdmin(admin.ModelAdmin):
    list_display = ('type_avion','nb_moteurs',)

class PiloteAdmin(admin.ModelAdmin):
    list_display = ('prenom','nom',)

admin.site.register(CodeAita,CodeAitaAdmin)
admin.site.register(TypeAvion,TypeAvionAdmin)
admin.site.register(Immatriculation,ImmatriculationAdmin)
admin.site.register(Pilote,PiloteAdmin)
admin.site.register(Vol,VolAdmin)