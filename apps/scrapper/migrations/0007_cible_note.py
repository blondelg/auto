# Generated by Django 3.1.1 on 2020-11-01 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapper', '0006_auto_20201021_2015'),
    ]

    operations = [
        migrations.AddField(
            model_name='cible',
            name='NOTE',
            field=models.IntegerField(default=0),
        ),
    ]