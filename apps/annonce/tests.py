from datetime import datetime, timedelta
from django.test import TestCase
from .models import Annonce
from apps.scrapper.models import Url
from apps.scrapper.models import Cible 


class AnnonceTestCase(TestCase):

    cible = Cible(DOMAINE = "www.lacentrale.fr", CIBLE = "lacentrale")
    cible.save()                          

    url = Url(URL = 'https://www.lacentrale.fr/auto-occasion-annonce-69106808446.html')

    data_annonce = {'URL': url, 
                    'PRIX': 10990, 
                    'MARQUE': 'AUDI', 
                    'MODELE': 'A3', 
                    'ENERGIE': 'DIESEL', 
                    'ANNEE': '2015', 
                    'CODEPOSTAL': '41190', 
                    'DIN': 110, 
                    'KM': 160990, 
                    'DATE': datetime(2020, 7, 28, 8, 15, 17, 987362)
    }
                              
        
    def test_get_age(self):

        test_annonce = Annonce(**self.data_annonce)
        self.assertEqual(isinstance(test_annonce.get_age(), int), True)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
