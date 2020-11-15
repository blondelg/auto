from django.test import TestCase
from django.conf import settings
from urllib.parse import urlparse

from apps.scrapper.scrapper import GetHtmlSession
from apps.scrapper.toolbox import toolbox_chooser
from apps.scrapper.scrapper import AnnonceListScrapper
from apps.scrapper.models import Url
from apps.scrapper.models import Cible 


class GetHtmlSessionTestCase(TestCase):

    real_url = Url(URL = 'https://www.python.org/')
    fake_url = Url(URL = 'https://www.fromage-de-chevre-bulgare.org/')
    

    html_lacentrale = r"""<label id="trackingStateContainer" style="display: none;">{"seller":{"ref":"C027193","type":"CENTRE_MULTIMARQUES","city":"PRAY","siret":"52898458600016"},"vehicle":{"vertical":"auto","price":{"price":10990,"isCrossed":false,"isDropping":false},"options":[{"label":"rétroviseurs électriques"},{"label":"aide parking"},{"label":"ordinateur de bord"},{"label":"jantes alu 16\""},{"label":"climatisation automatique"},{"label":"airbags frontaux"},{"label":"Bluetooth"},{"label":"Batterie + bougie allumage fait a 160214 KM"},{"label":"accoudoir central"},{"label":"fermeture électrique"},{"label":"radar arrière de détection d'obstacles"},{"label":"feux automatiques"},{"label":"banquette 1/3 - 2/3"},{"label":"fixations ISOFIX"},{"label":"système Start & Stop"},{"label":"projecteurs antibrouillard"},{"label":"régulateur de vitesse"},{"label":"contrôle de pression des pneus"},{"label":"vitres électriques"},{"label":"Filtre à air + Charge climatiseur + Balais d'essuie-glace AV + Révision fait en Juillet 2019 à 152123 Km"},{"label":"direction assistée"},{"label":"5 places"},{"label":"Disques de freins AV + Volant moteur + Embrayage fait à 160816 Km"},{"label":"ABS"},{"label":"GPS"}],"make":"AUDI","model":"A3","version":"III SPORTBACK 1.6 TDI 110 BUSINESS LINE","commercialName":"A3 (3E GENERATION) SPORTBACK","category":"COMPACTE","gearboxId":"MANUAL","energy":"DIESEL","isRecoverableVAT":false,"year":"2015","externalColor":"gris","firstHand":true,"doors":5,"cubic":1598,"zipcode":"41190","powerDIN":110,"ratedHorsePower":5,"mileage":160990,"fourWheels":false,"length":4310,"width":1790,"photos":[],"covidMeasures":["1","3"]},"classified":{"id":"69106808446","ref":"E106808446","ownerCorrelationId":"C027193","hasPriority":true,"hasColorOption":false,"hasBoldOption":false,"hasPicture":false,"hasPhoto360":false,"hasVisideoOption":false,"url":"https://www.lacentrale.fr/auto-occasion-annonce-69106808446.html","notFound":false,"priceIsDropping":false}}</div><div class="cbm-toolboxButtons">
<span>
Publié depuis : <strong>60 jours</strong>
</span>
</div>
<li class="arrow-btn "><a href="/occasion-voiture-marque-citroen-2.html" title="Page suivante"><i class="cbm-picto--arrowR"></i></a></li>
"""

    params = {}
    params['session_timeout'] = 1
    params['max_proxy_try'] = 2
    params['min_sleep_time'] = 0
    params['max_sleep_time'] = 1
    
    # GENERAL TESTS

    def test_retuns_text_real_url(self):
        self.session = GetHtmlSession(self.real_url.URL, **self.params)
        self.assertEqual(isinstance(self.session.get_html_text(), str), True)
        
        
    def test_retuns_text_fake_url(self):
        self.session = GetHtmlSession(self.fake_url.URL, **self.params)
        self.assertEqual(isinstance(self.session.get_html_text(), str), True)
        
        
    # TEST SOURCE LACENTRALE

    
    def test_returns_empty_dict_if_missing_data(self):
        url_parsed = urlparse('https://www.lacentrale.fr/')
        toolbox = toolbox_chooser(url_parsed)
        self.assertEqual(toolbox.get_data_from_html("some_html"), {})
        
    def test_returns_full_dict_if_data_are_ok(self):
        url_parsed = urlparse('https://www.lacentrale.fr/')
        toolbox = toolbox_chooser(url_parsed)
        self.assertEqual(isinstance(toolbox.get_data_from_html(self.html_lacentrale), dict), True)
         
    def test_get_next_page_url(self): 
        url_parsed = urlparse('https://www.lacentrale.fr/')
        toolbox = toolbox_chooser(url_parsed)
        self.assertEqual(isinstance(toolbox.get_next_page_url(self.html_lacentrale) , str), True)
        
    def test_get_random_url_existing(self):

        # set a fake source for tests
        cible = Cible(DOMAINE="www.tests.fr", CIBLE="tests")
        cible.save()
        # record tests urls
        cible = Cible.objects.get(CIBLE='tests')
        self.real_url.CIBLE = cible 
        self.fake_url.CIBLE = cible
        self.real_url.save()
        self.fake_url.save()
        random_url = Url()
        self.assertIsInstance(random_url.get_random_url(), Url)

    def test_get_random_url_not_existing(self):
        random_url = Url()
        self.assertIsNone(random_url.get_random_url('some-status'))
