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
    CIBLE = models.CharField(max_length=15)

    
    def __repr__(self):
        return f'<Url: {self.URL} | {self.STATUS}>'

    def __str__(self):
        return f'<Url: {self.URL} | {self.STATUS}>'
        
    def save(self, *args, **kwargs):
        """ prevent saving twice the same url """
        if Url.objects.filter(URL=self.URL).count() == 0:
            super(Url, self).save(*args, **kwargs)
        else:
            settings.LOGGER.warning(f"url deja en base {self.URL}")
    
    def get_last_entry_date(self):
       return Url.objects.only("DATE").aggregate(models.Max('DATE'))['DATE__max']
