from django.conf import settings
from datetime import datetime
from django.db import models



class Url(models.Model):
    STATUS_CHOIX = [
        ('ATTENTE', 'ATTENTE'),
        ('VALIDE', 'VALIDE'),
        ('ERREUR', 'ERREUR'),
    ]
    
    URL = models.URLField(max_length=500)
    STATUS = models.CharField(max_length=10, choices=STATUS_CHOIX, default='ATTENTE',)
    DATE = models.DateField(auto_now_add=True)
    CIBLE = models.ForeignKey('Cible', on_delete=models.CASCADE)

    
    def __repr__(self):
        return f'<Url: {self.URL} | {self.STATUS}>'

    def __str__(self):
        return f'<Url: {self.URL} | {self.STATUS}>'
        
    def save(self, *args, **kwargs):
        pass

    def get_last_entry_date(self):
       return Url.objects.only("DATE").aggregate(models.Max('DATE'))['DATE__max']

    def get_target_from_url(self):
        """ from a given url, retunrs a Cible object """
        
    class Meta:
        unique_together = ['URL']


class Cible(models.Model):
    DOMAINE = models.URLField(max_length=20)
    CIBLE = models.URLField(max_length=20)
    
    class Meta:
        unique_together = ['DOMAINE', 'CIBLE']

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except:
            pass
