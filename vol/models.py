from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class CodeIata(models.Model):
    code_iata = models.CharField(
        verbose_name='Code IATA',
        max_length=5,
    )
    ville = models.CharField(
        verbose_name="Ville",
        max_length=50,
        blank=True,
        null=True,
    )
    user_id = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='%(class)s_utilisateur',
        verbose_name="Utilisateur",
    )

    def __str__(self):
        return self.code_iata


class TypeAvion(models.Model):
    NOMBRE_MOTEURS = (
        ('1', 'Monomoteur'),
        ('2', 'Multimoteurs'),
    )
    type_avion = models.CharField(
        verbose_name='Type d\'avion',
        max_length=255,
    )
    nb_moteurs = models.CharField(
        choices=NOMBRE_MOTEURS,
        max_length=25,
        verbose_name='Nombre de moteurs',
    )
    user_id = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='%(class)s_utilisateur',
        verbose_name="Utilisateur",
    )

    def __str__(self):
        return self.type_avion


class Immatriculation(models.Model):
    immatriculation = models.CharField(
        verbose_name='Immatriculation de l\'avion',
        max_length=10,
    )
    type_avion = models.ForeignKey(
        TypeAvion,
        on_delete=models.PROTECT
    )
    user_id = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='%(class)s_utilisateur',
        verbose_name="Utilisateur",
    )

    def __str__(self):
        return self.immatriculation


class Pilote(models.Model):
    prenom = models.CharField(
        verbose_name='Prénom',
        max_length=255,
    )
    nom = models.CharField(
        verbose_name='Nom de famille',
        max_length=255,
    )
    user_id = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='%(class)s_utilisateur',
        verbose_name="Utilisateur",
    )

    def __str__(self):
        return '%s %s' % (self.prenom, self.nom)


class Vol(models.Model):
    FONCTION = (
        ('PF', 'Pilot Flying'),
        ('PNF', 'Pilot Non Flying'),
        ('MIX', 'Mix'),
    )
    POSTE = (
        ('CDB', 'Commandant de bord'),
        ('OPL', 'Copilote'),
        ('Instruct', 'Instructeur'),
        ('OBS', 'Observateur'),
    )
    ZERO = 0
    UN = 1
    DEUX = 2
    ARRIVEE_IFR = (
        ('Zéro', ZERO),
        ('Un', UN),
        ('Deux', DEUX),
    )
    
    date = models.DateField(
        verbose_name = 'Date du vol',
    )
    cdb = models.ForeignKey(
        Pilote, 
        on_delete=models.PROTECT,
        related_name='%(class)s_cdb',
        verbose_name="Commandant de bord",
    )
    opl = models.ForeignKey(
        Pilote, 
        on_delete=models.PROTECT,
        related_name='%(class)s_opl',
        verbose_name="Copilote",
    )
    obs1 = models.ForeignKey(
        Pilote, 
        on_delete=models.PROTECT,
        related_name='%(class)s_obs1',
        verbose_name="Observateur 1",
        blank=True,
        null=True,
    )
    obs2 = models.ForeignKey(
        Pilote, 
        on_delete=models.PROTECT,
        related_name='%(class)s_obs2',
        verbose_name="Observateur 2",
        blank=True,
        null=True,
    )
    instructeur = models.ForeignKey(
        Pilote, 
        on_delete=models.PROTECT,
        related_name='%(class)s_instructeur',
        verbose_name="Instructeur",
        blank=True,
        null=True,
    )
    depart = models.ForeignKey(
        CodeIata, 
        on_delete=models.PROTECT,
        related_name='%(class)s_depart',
        verbose_name = "Départ",
    )
    arrivee = models.ForeignKey(
        CodeIata, 
        on_delete=models.PROTECT,
        related_name='%(class)s_arrivee',
        verbose_name = "Arrivée",
    )
    duree_jour = models.DurationField(
        verbose_name="Vol de jour",
        blank=True,
        null=True,
        help_text='Format hh:mm:ss'
    )
    duree_nuit = models.DurationField(
        verbose_name="Vol de nuit",
        blank=True,
        null=True,
        help_text='Format hh:mm:ss'
    )
    fonction = models.CharField(
        choices = FONCTION,
        verbose_name = 'Fonction occupée',
        max_length = 20,
    )
    poste = models.CharField(
        choices = POSTE,
        verbose_name = 'Poste occupé',
        max_length = 20,
    )
    immatriculation = models.ForeignKey(
        Immatriculation, 
        on_delete=models.PROTECT,
        related_name='%(class)s_immatriculation',
        verbose_name="Immatriculation de l'avion",
    )
    observation = models.TextField(
        verbose_name="Observations",
        blank=True,
    )
    vol_ifr = models.CharField(
        choices = ARRIVEE_IFR,
        verbose_name = "Nombre d'arrivée IFR",
        max_length = 20,
        default = 1,
    )
    duree_ifr = models.DurationField(
        verbose_name="Durée IFR",
        blank=True,
        null=True,
        help_text='Format hh:mm:ss'
    )
    vol_dc = models.BooleanField(
        verbose_name="Vol DC ?",
        default=False,
    )
    duree_dc = models.DurationField(
        verbose_name="Durée DC",
        blank=True,
        null=True,
        help_text='Format hh:mm:ss'
    )
    vol_simu = models.BooleanField(
        verbose_name="Simulateur ?",
        default=False,
    )
    duree_simu = models.DurationField(
        verbose_name="Durée Simu",
        blank=True,
        null=True,
        help_text='Format hh:mm:ss'
    )
    user_id = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='%(class)s_utilisateur',
        verbose_name="Utilisateur",
        )
