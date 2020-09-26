from datetime import datetime, timedelta
from django.test import TestCase
from .models import Annonce


class AnnonceTestCase(TestCase):

    data = {'URL': 'https://www.lacentrale.fr/auto-occasion-annonce-69106808446.html', 
                              'PRIX': 10990, 
                              'MARQUE': 'AUDI', 
                              'MODELE': 'A3', 
                              'ENERGIE': 'DIESEL', 
                              'ANNEE': '2015', 
                              'CODEPOSTAL': '41190', 
                              'DIN': 110, 
                              'KM': 160990, 
                              'DATE': datetime(2020, 7, 28, 8, 15, 17, 987362)}
                              
    #test_annonce.save()

    
    def test_do_not_save_existing_url(self):
        
        test_annonce = Annonce(**self.data)
        test_annonce.save()
        
        test_annonce_2 = Annonce(**self.data)
        test_annonce_2.save()
        
        self.assertEqual(Annonce.objects.filter(URL=self.data['URL']).count(), 1)
        
    def test_get_age(self):

        test_annonce = Annonce(**self.data)
        self.assertEqual(isinstance(test_annonce.get_age(), int), True)
