# Generated by Django 2.1.3 on 2018-12-03 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vol', '0008_auto_20181203_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vol',
            name='observation',
            field=models.TextField(blank=True, verbose_name='Observations'),
        ),
    ]
