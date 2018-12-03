# Generated by Django 2.1.3 on 2018-12-03 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vol', '0005_delete_fonction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vol',
            name='poste',
            field=models.CharField(choices=[('CDB', 'Commandant de bord'), ('OPL', 'Copilote'), ('Instruct', 'Instructeur'), ('OBS', 'Observateur')], max_length=20, verbose_name='Nom du poste'),
        ),
        migrations.DeleteModel(
            name='Poste',
        ),
    ]
