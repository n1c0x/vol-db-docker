# Generated by Django 2.1.4 on 2018-12-04 11:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vol', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vol',
            name='duree_ifr',
        ),
    ]
