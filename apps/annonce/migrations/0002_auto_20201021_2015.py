# Generated by Django 3.1.1 on 2020-10-21 20:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrapper', '0006_auto_20201021_2015'),
        ('annonce', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='annonce',
            unique_together={('URL',)},
        ),
    ]