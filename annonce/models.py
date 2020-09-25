from django.db import models


class Annonce(models.Model):
    ENERGIE_CHOIX = [
        ('ESSENCE', 'ESSENCE'),
        ('DIESEL', 'DIESEL'),
    ]
    URLS = models.URLField(max_length=500)
    MARQUE = models.CharField(max_length=20, blank=True)
    MODELE = models.CharField(max_length=20, blank=True)
    KM = models.FloatField(blank=True)
    DIN = models.FloatField(blank=True)
    PRIX = models.FloatField(blank=True)
    ENERGIE = models.CharField(max_length=10, choices=ENERGIE_CHOIX, default='ESSENCE')
    ANNEE = models.IntegerField(blank=True)
    DATE = models.DateField()
