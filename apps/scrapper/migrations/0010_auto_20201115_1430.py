# Generated by Django 3.1.1 on 2020-11-15 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapper', '0009_auto_20201109_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cible',
            name='CIBLE',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='cible',
            name='DOMAINE',
            field=models.CharField(max_length=20),
        ),
    ]
