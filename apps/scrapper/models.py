from urllib.parse import urlparse
from django.conf import settings
from datetime import datetime
from django.db import models
import random


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
        """ if CIBLE field is empty, tryes to find it in Cible table """
        try:
            super(Url, self).save(*args, **kwargs)
        except:
            self.CIBLE = self.get_target_from_url()
            super(Url, self).save(*args, **kwargs)
            
         

    def get_last_entry_date(self):
       return Url.objects.only("DATE").aggregate(models.Max('DATE'))['DATE__max']

    def get_target_from_url(self):
        """ from a given url, retunrs a Cible object """
        domaine = urlparse(self.URL).netloc
        return Cible.objects.get(DOMAINE = domaine)

    def get_random_url(self, status='ATTENTE'):
        """ retunrs a random url ubject """
        pk_queryset = Url.objects.filter(STATUS=status).values_list("pk")
        pk_list = [e[0] for e in list(pk_queryset)]
        if len(pk_list) == 0:
            return None 
        else:
            pk_random = random.choice(pk_list)
            return Url.objects.get(pk=pk_random)

    def has_status(self, status='ATTENTE'):
        """ returns True if there is some urls with th
        corresponding status"""
        count = Url.objects.filter(STATUS=status).count()
        if count == 0:
            return False
        else:
            return True
        
    class Meta:
        unique_together = ['URL']


class Cible(models.Model):
    DOMAINE = models.CharField(max_length=20)
    CIBLE = models.CharField(max_length=20)
    
    def __repr__(self):
        return f'<Cible: {self.CIBLE}>'

    def __str__(self):
        return f'<Cible: {self.CIBLE}>'
    
    class Meta:
        unique_together = ['DOMAINE', 'CIBLE']

    def save(self, *args, **kwargs):
        """ don't save if record exists """
        try:
            super().save(*args, **kwargs)
        except:
            pass
            
            
            
