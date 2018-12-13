# Generated by Django 2.1.4 on 2018-12-04 10:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CodeAita',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_aita', models.CharField(max_length=5, verbose_name='Code Aita')),
                ('ville', models.CharField(blank=True, max_length=50, null=True, verbose_name='Ville')),
            ],
        ),
        migrations.CreateModel(
            name='Immatriculation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('immatriculation', models.CharField(max_length=10, verbose_name="Immatriculation de l'avion")),
            ],
        ),
        migrations.CreateModel(
            name='Pilote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prenom', models.CharField(max_length=255, verbose_name='Prénom')),
                ('nom', models.CharField(max_length=255, verbose_name='Nom de famille')),
            ],
        ),
        migrations.CreateModel(
            name='TypeAvion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_avion', models.CharField(max_length=255, verbose_name="Type d'avion")),
                ('nb_moteurs', models.CharField(choices=[('1', 'Monomoteur'), ('2', 'Multimoteurs')], max_length=25, verbose_name='Nombre de moteurs')),
            ],
        ),
        migrations.CreateModel(
            name='Vol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Date du vol')),
                ('duree_jour', models.DurationField(verbose_name='Durée de vol de jour')),
                ('duree_nuit', models.DurationField(verbose_name='Durée de vol de nuit')),
                ('duree_ifr', models.DurationField(verbose_name='Durée de vol IFR')),
                ('arrivee_ifr', models.BooleanField(verbose_name='Arrivée IFR ?')),
                ('fonction', models.CharField(choices=[('PF', 'PF'), ('PNF', 'PNF'), ('MIX', 'MIX')], max_length=3, verbose_name='Fonction occupée')),
                ('poste', models.CharField(choices=[('CDB', 'Commandant de bord'), ('OPL', 'Copilote'), ('Instruct', 'Instructeur'), ('OBS', 'Observateur')], max_length=20, verbose_name='Poste occupé')),
                ('observation', models.TextField(blank=True, verbose_name='Observations')),
                ('simu', models.BooleanField(verbose_name='Simulateur ?')),
                ('arrivee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='vol_arrivee', to='vol.CodeAita', verbose_name='Arrivée')),
                ('cdb', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='vol_cdb', to='vol.Pilote', verbose_name='Commandant de bord')),
                ('depart', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='vol_depart', to='vol.CodeAita', verbose_name='Départ')),
                ('immatriculation', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='vol_immatriculation', to='vol.Immatriculation', verbose_name="Immatriculation de l'avion")),
                ('instructeur', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='vol_instructeur', to='vol.Pilote', verbose_name='Instructeur')),
                ('obs1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='vol_obs1', to='vol.Pilote', verbose_name='Observateur 1')),
                ('obs2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='vol_obs2', to='vol.Pilote', verbose_name='Observateur 2')),
                ('opl', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='vol_opl', to='vol.Pilote', verbose_name='Copilote')),
            ],
        ),
        migrations.AddField(
            model_name='immatriculation',
            name='type_avion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='vol.TypeAvion'),
        ),
    ]