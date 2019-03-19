from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _
from django.urls import reverse


class Profile(models.Model):
    CLIENT_TYPE = (
        ('Gratuit', 'Gratuit'),
        ('Payant', 'Payant'),
    )
    CURRENT_POSITION = (
        ('CDB', 'Commandant de bord'),
        ('OPL', 'Copilote'),
        ('INSTRUC', 'Instructeur'),
        ('RETR', 'Retraité'),
        ('AUTRE', 'Autre'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    client_type = models.CharField(
        choices=CLIENT_TYPE,
        max_length=25,
        verbose_name='Type de client',
    )
    current_position = models.CharField(
        choices=CURRENT_POSITION,
        max_length=25,
        verbose_name='Poste actuel',
    )
    employer = models.CharField(
        max_length=25,
        verbose_name='Employeur',
    )

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class CodeIata(models.Model):
    """ Define IATA codes table. """
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

    class Meta:
        ordering = ('code_iata',)

    def __str__(self):
        return self.code_iata

    def save(self, force_insert=False, force_update=False):
        self.code_iata = self.code_iata.upper()
        super(CodeIata, self).save(force_insert, force_update)


class TypeAvion(models.Model):
    """ Define plane type table """
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

    class Meta:
        ordering = ('type_avion',)

    def __str__(self):
        return self.type_avion

    def save(self, force_insert=False, force_update=False):
        self.type_avion = self.type_avion.upper()
        super(TypeAvion, self).save(force_insert, force_update)


class Immatriculation(models.Model):
    """ Define immatriculation table. """
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

    class Meta:
        ordering = ('immatriculation',)

    def __str__(self):
        return self.immatriculation

    # def __str__(self):
    #     return self.immatriculation + " (" + self.type_avion.type_avion + ")"

    def save(self, force_insert=False, force_update=False):
        self.immatriculation = self.immatriculation.upper()
        super(Immatriculation, self).save(force_insert, force_update)

    def get_absolute_url(self):
        return reverse('immatriculation', kwargs={'pk': self.pk})


class Pilote(models.Model):
    """ Define pilot table. """
    POSTE = (
        ('CDB', 'Commandant de bord'),
        ('OPL', 'Copilote'),
        ('Instruct', 'Instructeur'),
        ('OBS', 'Observateur'),
    )
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

    class Meta:
        ordering = ('nom', 'prenom')

    def __str__(self):
        return '%s %s' % (self.nom, self.prenom)


class Vol(models.Model):
    """ Define flight table. """
    FONCTION = (
        ('PF', 'Pilot Flying'),
        ('PM (PNF)', 'Pilot Monitoring (Pilot Non Flying)'),
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
        ('0', ZERO),
        ('1', UN),
        ('2', DEUX),
    )

    date = models.DateField(
        verbose_name='Date du vol',
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
        verbose_name="Départ",
    )
    arrivee = models.ForeignKey(
        CodeIata,
        on_delete=models.PROTECT,
        related_name='%(class)s_arrivee',
        verbose_name="Arrivée",
    )
    duree_jour = models.DurationField(
        null=True,
        blank=True,
        verbose_name=_('duree_jour'),
        help_text=_('[DD] [HH:[MM:]]ss[.uuuuuu] format')
    )

    def duree_jour_HHmm(self):
        sec = self.duree_jour.total_seconds()
        return '%02d:%02d' % (int((sec / 3600) % 3600), int((sec / 60) % 60))

    duree_nuit = models.DurationField(
        null=True,
        blank=True,
        verbose_name=_('duree_nuit'),
        help_text=_('[DD] [HH:[MM:]]ss[.uuuuuu] format')
    )

    def duree_nuit_HHmm(self):
        sec = self.duree_nuit.total_seconds()
        return '%02d:%02d' % (int((sec / 3600) % 3600), int((sec / 60) % 60))

    fonction = models.CharField(
        choices=FONCTION,
        verbose_name='Fonction occupée',
        max_length=20,
    )
    poste = models.CharField(
        choices=POSTE,
        verbose_name='Poste occupé',
        max_length=20,
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
        choices=ARRIVEE_IFR,
        verbose_name="Nombre d'arrivée IFR",
        max_length=20,
        default=1,
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
        help_text='Format hh:mm:ss',
    )
    user_id = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='%(class)s_utilisateur',
        verbose_name="Utilisateur",
    )
