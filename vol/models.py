from django.db import models

# Create your models here.

class CodeAita(models.Model):
    code_aita = models.CharField(
        verbose_name = 'Code Aita',
        max_length = 5,
    )
    ville = models.CharField(
        verbose_name = "Ville",
        max_length = 50,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.code_aita
    
class TypeAvion(models.Model):
    NOMBRE_MOTEURS = (
        ('1','Monomoteur'),
        ('2','Multimoteurs'),
    )
    type_avion = models.CharField(
        verbose_name = 'Type d\'avion',
        max_length  = 255,
    )
    nb_moteurs = models.CharField(
        choices = NOMBRE_MOTEURS,
        max_length = 25,
        verbose_name = 'Nombre de moteurs',
       )
    
    def __str__(self):
        return self.type_avion

class Immatriculation(models.Model):
    immatriculation = models.CharField(
        verbose_name = 'Immatriculation de l\'avion',
        max_length = 10,
    )
    type_avion = models.ForeignKey(
        TypeAvion,
        on_delete=models.PROTECT
    )
    
    def __str__(self):
        return self.immatriculation
 
class Pilote(models.Model):
    prenom = models.CharField(
        verbose_name = 'Prénom',
        max_length = 255,
    )
    nom = models.CharField(
        verbose_name = 'Nom de famille',
        max_length = 255,
    )

    def __str__(self):
        return '%s %s' % (self.prenom, self.nom)

class Vol(models.Model):
    FONCTION = (
        ('PF','Pilot Flying'),
        ('PNF','Pilot Non Flying'),
        ('MIX','Mix'),
    )
    POSTE = (
        ('CDB','Commandant de bord'),
        ('OPL','Copilote'),
        ('Instruct','Instructeur'),
        ('OBS','Observateur'),
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
        CodeAita, 
        on_delete=models.PROTECT,
        related_name='%(class)s_depart',
        verbose_name = "Départ",
    )
    arrivee = models.ForeignKey(
        CodeAita, 
        on_delete=models.PROTECT,
        related_name='%(class)s_arrivee',
        verbose_name = "Arrivée",
    )
    duree_jour = models.DurationField(
        verbose_name="Vol de jour",
    )
    duree_nuit = models.DurationField(
        verbose_name="Vol de nuit",
    )
    duree_ifr = models.DurationField(
        verbose_name="Vol IFR",
        blank=True,
        null=True,
    )
    arrivee_ifr = models.BooleanField(
        verbose_name="Arrivée IFR ?",
        default=False,
    )
    vol_dc = models.BooleanField(
        verbose_name="Vol en doubles commandes ?",
        default=False,
    )
    duree_dc = models.DurationField(
        verbose_name="Vol double commandes",
        blank=True,
        null=True,
    )
    fonction = models.CharField(
        choices = FONCTION,
        verbose_name = 'Fonction occupée',
        max_length = 3
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
    simu = models.BooleanField(
        verbose_name="Simulateur ?",
        default=False,
    )
    duree_simu = models.DurationField(
        verbose_name="Vol Simu",
        blank=True,
        null=True,
    )

