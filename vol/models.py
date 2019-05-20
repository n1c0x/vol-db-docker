from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

# from django.utils.duration import _get_duration_components
# from django.db.models.fields import DurationField


# class DurationField(DurationField):
#     def value_to_string(self, obj):
#         val = self.value_from_object(obj)
#         if val is None:
#             return ''
#         days, hours, minutes, seconds, microseconds = _get_duration_components(val)
#         return '{} days, {:02d} hours, {:02d} minutes, {:02d}.{:06d} seconds'.format(days, hours, minutes, seconds, microseconds)

#     def duration_string(duration):
#         """Version of str(timedelta) which is not English specific."""
#         days, hours, minutes, seconds, microseconds = _get_duration_components(duration)

#         return '{} days, {:02d} hours, {:02d} minutes, {:02d}.{:06d} seconds'.format(days, hours, minutes, seconds, microseconds)

#         string = '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)
#         if days:
#             string = '{} '.format(days) + string
#         if microseconds:
#             string += '.{:06d}'.format(microseconds)

#         return string


class Profile(models.Model):
    """ Define user profile """
    CLIENT_TYPE = (
        ('free', _('Free')),
        ('pay', _('Pay')),
    )
    CURRENT_POSITION = (
        ('PIC', _('Pilot in Command')),
        ('FO', _('First Officer')),
        ('INSTRUCT', _('Instructor')),
        ('RET', _('Retired')),
        ('OTHER', _('Other')),
    )
    LANGUAGE = (
        ('fr', _('French')),
        ('en', _('English')),
        ('de', _('German')),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    client_type = models.CharField(
        choices=CLIENT_TYPE,
        max_length=25,
        verbose_name=_('Client type'),
    )
    current_position = models.CharField(
        choices=CURRENT_POSITION,
        max_length=25,
        verbose_name=_('Current position'),
    )
    employer = models.CharField(
        max_length=25,
        verbose_name=_('Employer'),
    )
    language = models.CharField(
        choices=LANGUAGE,
        max_length=25,
        verbose_name=_('Language'),
        default='fr',
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
        verbose_name=_('IATA code'),
        max_length=5,
    )
    ville = models.CharField(
        verbose_name=_('City'),
        max_length=50,
        blank=True,
        null=True,
    )
    user_id = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='%(class)s_utilisateur',
        verbose_name=_('User'),
    )

    class Meta:
        ordering = ('code_iata',)
        verbose_name = _('IATA Code')
        verbose_name_plural = _('IATA Codes')
        constraints = [
            models.UniqueConstraint(fields=[
                'code_iata',
                'user_id'],
                name='code_iata_unique')
        ]

    def __str__(self):
        return self.code_iata

    def save(self, force_insert=False, force_update=False):
        self.code_iata = self.code_iata.upper()
        super(CodeIata, self).save(force_insert, force_update)


class TypeAvion(models.Model):
    """ Define plane type table """
    NOMBRE_MOTEURS = (
        (_('One'), _('Single-engine')),
        (_('Multiple'), _('Multi-engine')),
    )
    type_avion = models.CharField(
        verbose_name=_('Aircraft type'),
        max_length=255,
    )
    nb_moteurs = models.CharField(
        choices=NOMBRE_MOTEURS,
        max_length=25,
        verbose_name=_('Amount of engines'),
    )
    user_id = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='%(class)s_utilisateur',
        verbose_name=_('User'),
    )

    class Meta:
        ordering = ('type_avion',)
        verbose_name = _('Aircraft type')
        verbose_name_plural = _('Aircraft types')
        constraints = [
            models.UniqueConstraint(fields=[
                'type_avion',
                'user_id'],
                name='type_avion_unique')
        ]

    def __str__(self):
        return self.type_avion

    def save(self, force_insert=False, force_update=False):
        self.type_avion = self.type_avion.upper()
        super(TypeAvion, self).save(force_insert, force_update)


class Immatriculation(models.Model):
    """ Define immatriculation table. """
    immatriculation = models.CharField(
        verbose_name=_('Registration number'),
        max_length=10,
    )
    type_avion = models.ForeignKey(
        TypeAvion,
        verbose_name=_('Aircraft type'),
        on_delete=models.PROTECT
    )
    user_id = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='%(class)s_utilisateur',
        verbose_name=_('User'),
    )

    class Meta:
        ordering = ('immatriculation',)
        verbose_name = _('Registration Number')
        verbose_name_plural = _('Registration Numbers')
        constraints = [
            models.UniqueConstraint(fields=[
                'immatriculation',
                'user_id'],
                name='immatriculation_unique')
        ]

    def __str__(self):
        return self.immatriculation

    def save(self, force_insert=False, force_update=False):
        self.immatriculation = self.immatriculation.upper()
        super(Immatriculation, self).save(force_insert, force_update)

    def get_absolute_url(self):
        return reverse('immatriculation', kwargs={'pk': self.pk})


class Pilote(models.Model):
    """ Define pilot table. """
    POSTE = (
        (_('PIC'), _('Pilot in Command')),
        (_('FO'), _('First Officer')),
        (_('Instruct'), _('Instructor')),
        (_('OBS'), _('Observer')),
    )
    prenom = models.CharField(
        verbose_name=_('First name'),
        max_length=255,
    )
    nom = models.CharField(
        verbose_name=_('Family name'),
        max_length=255,
    )
    user_id = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='%(class)s_utilisateur',
        verbose_name=_('User'),
    )

    class Meta:
        ordering = ('nom', 'prenom')
        verbose_name = _('Pilot')
        verbose_name_plural = _('Pilots')
        constraints = [
            models.UniqueConstraint(fields=[
                'prenom',
                'nom',
                'user_id'],
                name='pilot_unique')
        ]

    def __str__(self):
        return '%s %s' % (self.prenom, self.nom)


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
        verbose_name=_('Flight date'),
    )
    cdb = models.ForeignKey(
        Pilote,
        on_delete=models.PROTECT,
        related_name='%(class)s_cdb',
        verbose_name=_('Pilot in Command'),
    )
    opl = models.ForeignKey(
        Pilote,
        on_delete=models.PROTECT,
        related_name='%(class)s_opl',
        verbose_name=_('First officer'),
    )
    obs1 = models.ForeignKey(
        Pilote,
        on_delete=models.PROTECT,
        related_name='%(class)s_obs1',
        verbose_name=_('Observer 1'),
        blank=True,
        null=True,
    )
    obs2 = models.ForeignKey(
        Pilote,
        on_delete=models.PROTECT,
        related_name='%(class)s_obs2',
        verbose_name=_('Observer 2'),
        blank=True,
        null=True,
    )
    instructeur = models.ForeignKey(
        Pilote,
        on_delete=models.PROTECT,
        related_name='%(class)s_instructeur',
        verbose_name=_('Instructor'),
        blank=True,
        null=True,
    )
    depart = models.ForeignKey(
        CodeIata,
        on_delete=models.PROTECT,
        related_name='%(class)s_depart',
        verbose_name=_('Departure'),
    )
    arrivee = models.ForeignKey(
        CodeIata,
        on_delete=models.PROTECT,
        related_name='%(class)s_arrivee',
        verbose_name=_('Arrival'),
    )
    duree_jour = models.DurationField(
        null=True,
        blank=True,
        verbose_name=_('Day duration'),
        help_text=_('[DD] [HH:[MM:]]ss[.uuuuuu] format')
    )

    def duree_jour_HHmm(self):
        sec = self.duree_jour.total_seconds()
        return '%02d:%02d' % (int((sec / 3600) % 3600), int((sec / 60) % 60))

    duree_nuit = models.DurationField(
        null=True,
        blank=True,
        verbose_name=_('Night duration'),
        help_text=_('[DD] [HH:[MM:]]ss[.uuuuuu] format')
    )

    def duree_nuit_HHmm(self):
        sec = self.duree_nuit.total_seconds()
        return '%02d:%02d' % (int((sec / 3600) % 3600), int((sec / 60) % 60))

    fonction = models.CharField(
        choices=FONCTION,
        verbose_name=_('Function'),
        max_length=20,
    )
    poste = models.CharField(
        choices=POSTE,
        verbose_name=_('Position'),
        max_length=20,
    )
    immatriculation = models.ForeignKey(
        Immatriculation,
        on_delete=models.PROTECT,
        related_name='%(class)s_immatriculation',
        verbose_name=_('Registration number'),
    )
    observation = models.TextField(
        verbose_name=_('Notes'),
        blank=True,
    )
    vol_ifr = models.CharField(
        choices=ARRIVEE_IFR,
        verbose_name=_('IFR arrivals'),
        max_length=20,
        default=1,
    )
    duree_ifr = models.DurationField(
        verbose_name=_('IFR duration'),
        blank=True,
        null=True,
        help_text='Format hh:mm:ss'
    )
    vol_dc = models.BooleanField(
        verbose_name=_('DC flight'),
        default=False,
    )
    duree_dc = models.DurationField(
        verbose_name=_('DC duration'),
        blank=True,
        null=True,
        help_text='Format hh:mm:ss'
    )
    vol_simu = models.BooleanField(
        verbose_name=_('Simulator'),
        default=False,
    )
    duree_simu = models.DurationField(
        verbose_name=_('Simu duration'),
        blank=True,
        null=True,
        help_text='Format hh:mm:ss',
    )
    user_id = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='%(class)s_utilisateur',
        verbose_name="User",
    )
