from datetime import datetime, timedelta
from apps.annonce.models import Annonce 
from fake_useragent import UserAgent
from django.conf import settings
from bs4 import BeautifulSoup
from .models import Url
import itertools as it
import requests
import random
import time
import json



# Decorator that makes soup from html
def soup(func):
    def get_soup(*args, **kwargs):
        kwargs['soup'] = BeautifulSoup(args[1], "html.parser")
        return func(*args, **kwargs)
    return get_soup


class GetHtmlSession:
    """ Build session and retrieve html source """
    
    def __init__(self, url, **kwargs):
        self.proxy_count = 0
        self.proxy_num = 0
        self.url = url
        self.user_agent = UserAgent()
        self.status_code = 0
        self.err = ''

        # Change default settings if needed
        self.session_timeout = kwargs.get('session_timeout',
                int(settings.CONFIG['SCRAPPER']['session_timeout']))
        self.max_proxy_try = kwargs.get('max_proxy_try',
                int(settings.CONFIG['SCRAPPER']['max_proxy_try']))
        self.min_sleep_time = kwargs.get('min_sleep_time',
                int(settings.CONFIG['SCRAPPER']['min_sleep_time']))
        self.max_sleep_time = kwargs.get('max_sleep_time',
                int(settings.CONFIG['SCRAPPER']['max_sleep_time']))

        # Get proxies
        self.get_proxies()
        
        # Get response
        self.get_response()
        
        
    def get_response(self):
        """ 
        Submit request until response is 200 
        Use proxies and User agent
        """
        try_count = 1
        start = time.time()
        while self.status_code != 200:
            
            # Setup proxy and header for get request
            session = requests.Session()
            session.proxies = {"http": f"http://{self.get_proxy_http()}", 
                               "https": f"https://{self.get_proxy_https()}"}
            headers = requests.utils.default_headers()
            headers.update({'User-Agent': self.user_agent.random})
            session.headers = headers
            
            # Submit request
            try:
                time.sleep(random.randrange(self.min_sleep_time,self.max_sleep_time))
                
                self.response = session.get(self.url, timeout=self.session_timeout)
                self.status_code = self.response.status_code
                
            except requests.exceptions.RequestException as err:
                self.response = requests.Response()
                self.err = err
            
            # Exit if too many fail
            if self.response.status_code == 200:
                end = time.time()
                settings.LOGGER.info(f"Exit code 200 after {try_count} tries")
                settings.LOGGER.info(f"Response in {end - start} seconds")

            elif self.response.status_code != 200 and try_count == self.max_proxy_try:
                settings.LOGGER.error(f"get request exceded {try_count} tries")
                settings.LOGGER.error(f"request error {self.err}")
                settings.LOGGER.error(f"headers {session.headers}")
                settings.LOGGER.error(f"proxies {session.proxies}")
                settings.LOGGER.error(f"url {self.url}")
                break
                
            try_count += 1


    def get_proxies(self):
        """ Get proxies list """
        
        try:
            url_http = 'https://www.proxy-list.download/api/v1/get?type=http'
            response = requests.get(url_http, timeout=self.session_timeout)
            proxy_list = response.text.split("\r\n")
            self.proxy_pool_http = it.cycle(proxy_list)

            url_https = 'https://www.proxy-list.download/api/v1/get?type=https'
            response = requests.get(url_https, timeout=self.session_timeout)
            proxy_list = response.text.split("\r\n")
            self.proxy_pool_https = it.cycle(proxy_list)
            
            self.proxy_num = len(proxy_list)
            self.proxy_count = 0
            
        except Exception as err:
            settings.LOGGER.error(f"proxy error {err}")

        
    def get_proxy_http(self):
        """ 
        Give a proxy from list
        Check if proxy list has to be refreshed
        """
        
        if self.proxy_count > self.proxy_num: self.get_proxies()
        return next(self.proxy_pool_http)
    
    
    def get_proxy_https(self):
        """ 
        Give a proxy from list
        Count used proxies
        """
        
        self.proxy_count += 1
        return next(self.proxy_pool_https)

    
    def get_html_text(self):
        """ Return html as string """
        
        try:
            return self.response.text
        except:
            return ''
            

class DataParser:
    """ provides a set of methods to scrap data from an annonce """
    
    def __init__(self):
        pass
        
    @soup
    def scrap_lacentrale(self, html, **kwargs):
    
        try:
            #  print("KWARGS :", type(kwargs['soup']))
            json_data = json.loads(kwargs['soup'].find("label", {"id": "trackingStateContainer"}).getText())
            age = kwargs['soup'].find("div", {"class": "cbm-toolboxButtons"}).span.strong.getText().strip().split(" ")[0]
            DATE = datetime.now() - timedelta(days=int(age))
            #  output = {'URL': json_data['classified']['url'],
            output = {'PRIX': json_data['vehicle']['price']['price'],
                    'MARQUE': json_data['vehicle']['make'],
                    'MODELE': json_data['vehicle']['model'],
                    'ENERGIE': json_data['vehicle']['energy'],
                    'ANNEE': json_data['vehicle']['year'],
                    'CODEPOSTAL': json_data['vehicle']['zipcode'],
                    'DIN': json_data['vehicle']['powerDIN'],
                    'KM': json_data['vehicle']['mileage'],
                    'DATE': DATE}
            return output
                    
        except Exception as err:
            settings.LOGGER.error(f"lacentrale {err}")
            return {}


class AnnonceListScrapper:
    """ From a search url """
    
    domain = "https://www.lacentrale.fr{}"
    
    def __init__(self, search_url, **kwargs):
        self.search_url = search_url
        self.kwargs = kwargs
        self.page_url = []
        self.ad_url = []
        self.get_page_urls(search_url)
        self.get_ad_urls()
        self.save_ad_urls()
        
    
    def get_page_urls(self, url):
        """ from a given search URL, retrieve all pagination urls """
        url = self.search_url
        
        while url:
            self.page_url.append(url)
            session = GetHtmlSession(url, **self.kwargs)
            url = self.get_next_page_url(session.get_html_text())


          
    def get_ad_urls(self):
        """ return a list with urls for all ads """
        for url in self.page_url:
            session = GetHtmlSession(url, **self.kwargs)
            self.get_ad_url_list(session.get_html_text())
            
            
    @soup
    def get_next_page_url(self, html, **kwargs):
        """ returns url of next page """
        for e in kwargs['soup'].find_all("li", {"class": "arrow-btn"}):
            if "suivante" in e.decode_contents():
                return self.domain.format(e.find("a")['href'])
        return None
        

    @soup
    def get_ad_url_list(self, html, **kwargs):
        """ update list of ad urls """
        for e in kwargs['soup'].find_all("div", {"class": "adContainer"}):
            sub_soup = BeautifulSoup(e.decode_contents(), "html.parser")
            self.ad_url.append(sub_soup.find("a")['href'])
            
    
    def save_ad_urls(self):
        """ from a list of urls record them in database """
        url_objects_list = []
        for url in self.ad_url:
            url_objects_list.append(Url(URL=self.domain.format(url)))
        Url.objects.bulk_create(url_objects_list)


class AnnonceScrapper:
    """ from a given ad url, scrape data into annonce table  """
    def __init__(self, url):
        self.url = url      
        self.get_data_from_url()
        self.save_annonce()

    def get_data_from_url(self):
        """ scrape data from url """
        session = GetHtmlSession(self.url.URL)
        html = session.get_html_text()
        parser = DataParser()
        self.data_dict = parser.scrap_lacentrale(html)

    def save_annonce(self):
        """ save data from dict into annonce table """
        try:
            annonce = Annonce(**self.data_dict)
            annonce.URL = self.url
            annonce.save()
            Url.objects.filter(pk=self.url.pk).update(STATUS = 'VALIDE')
        except Exception as err:
            settings.LOGGER.error(f"{err}")
            Url.objects.filter(pk=self.url.pk).update(STATUS = 'ERREUR')

















