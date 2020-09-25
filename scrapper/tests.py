from django.test import TestCase

from scrapper import GetHtmlSession


class GetHtmlSessionTestCase(TestCase):

    self.real_url = 'https://www.python.org/'
    self.fake_url = 'https://www.fromage-de-chevre-bulgare.org/'

    def retuns_text_real_url(self):
    
        session = GetHtmlSession(self.real_url)
        
    def retuns_text_fake_url(self):
    
        session = GetHtmlSession(self.fake_url)
