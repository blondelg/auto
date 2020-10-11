from django.conf import settings
from datetime import datetime
from django.db import models

from apps.scrapper.models import Url



class Annonce(models.Model):
    ENERGIE_CHOIX = [
        ('ESSENCE', 'ESSENCE'),
        ('DIESEL', 'DIESEL'),
    ]
    URL = models.ForeignKey(Url, on_delete=models.CASCADE)
    MARQUE = models.CharField(max_length=20, blank=True)
    MODELE = models.CharField(max_length=20, blank=True)
    KM = models.FloatField(blank=True)
    DIN = models.FloatField(blank=True)
    PRIX = models.FloatField(blank=True)
    ENERGIE = models.CharField(max_length=10, choices=ENERGIE_CHOIX, default='ESSENCE')
    ANNEE = models.IntegerField(blank=True)
    DATE = models.DateField()
    CODEPOSTAL = models.IntegerField(blank=True)
    
    def __repr__(self):
        return f'<Annonce: URL={self.URL}>'

    def __str__(self):
        return f'<Annonce: URL={self.URL}>'
    
    def save(self, *args, **kwargs):
        """ prevent saving ads with same URL """
        if Annonce.objects.filter(URL=self.URL).count() == 0:
            super(Annonce, self).save(*args, **kwargs)
        else:
            settings.LOGGER.warning(f"annonce deja en base {self.URL}")
            
    def get_age(self):
        """ returns ad age from today """
        d = datetime.now() - self.DATE
        return d.days
