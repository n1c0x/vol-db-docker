# Generated by Django 2.1.4 on 2018-12-04 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vol', '0002_remove_vol_duree_ifr'),
    ]

    operations = [
        migrations.AddField(
            model_name='vol',
            name='duree_ifr',
            field=models.DurationField(blank=True, null=True, verbose_name='Durée de vol IFR'),
        ),
    ]