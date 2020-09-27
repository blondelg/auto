from datetime import datetime, timedelta
from django.test import TestCase
from .models import Annonce
from scrapper.models import Url


class AnnonceTestCase(TestCase):

    data_annonce = {'URL': 'https://www.lacentrale.fr/auto-occasion-annonce-69106808446.html', 
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
                              
    data_url = {'URL': 'https://www.lacentrale.fr/auto-occasion-annonce-69106808446.html',
                'CIBLE': 'lacentrale'
    }
                              


    
    def test_do_not_save_existing_url(self):
        
        test_url = Url(**self.data_url)
        test_url.save()
        
        self.data_annonce['URL'] = test_url
        
        test_annonce = Annonce(**self.data_annonce)
        test_annonce.save()
        
        test_annonce_2 = Annonce(**self.data_annonce)
        test_annonce_2.save()
        
        self.assertEqual(Annonce.objects.filter(URL=test_url).count(), 1)
        
    def test_get_age(self):

        test_annonce = Annonce(**self.data_annonce)
        self.assertEqual(isinstance(test_annonce.get_age(), int), True)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
