# Generated by Django 3.1.1 on 2020-10-21 20:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrapper', '0005_auto_20201021_1839'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cible',
            unique_together={('DOMAINE', 'CIBLE')},
        ),
        migrations.AlterUniqueTogether(
            name='url',
            unique_together={('URL',)},
        ),
    ]