from datetime import datetime, timedelta
from fake_useragent import UserAgent
from django.conf import settings
from bs4 import BeautifulSoup
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
    
    def __init__(self, url):
        self.proxy_count = 0
        self.proxy_num = 0
        self.url = url
        self.user_agent = UserAgent().random
        self.status_code = 0
        self.session_timeout = int(settings.CONFIG['SCRAPPER']['session_timeout'])
        self.max_proxy_try = int(settings.CONFIG['SCRAPPER']['max_proxy_try'])
        
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
        while self.status_code != 200:
            
            # Setup proxy and header for get request
            session = requests.Session()
            session.proxies = {"http": f"http://{self.get_proxy_http()}", 
                               "https": f"https://{self.get_proxy_https()}"}
            headers = requests.utils.default_headers()
            headers.update({'user_agent': self.user_agent},)
            session.headers = headers
            
            # Submit request
            try:
                time.sleep(random.randrange(1,5))
                self.response = requests.get(self.url, timeout=self.session_timeout)
                self.status_code = self.response.status_code
                
            except requests.exceptions.RequestException as err:
                settings.LOGGER.error(f"request error {err}")
                self.response = requests.Response()
            
            # Exit if too many fail
            if self.response.status_code != 200 and try_count == self.max_proxy_try:
                settings.LOGGER.warning(f"get request exceded {try_count} tries")
                break
                
            try_count += 1


    def get_proxies(self):
        """ Get proxies list """
        
        try:
            url_http = 'https://www.proxy-list.download/api/v1/get?type=httpe'
            response = requests.get(url_http, timeout=self.session_timeout)
            proxy_list = response.text.split("\r\n")
            self.proxy_pool_http = it.cycle(proxy_list)

            url_https = 'https://www.proxy-list.download/api/v1/get?type=httpse'
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
            json_data = json.loads(kwargs['soup'].find("div", {"id": "trackingStateContainer"}).getText())
            age = kwargs['soup'].find("div", {"class": "cbm-toolboxButtons"}).span.strong.getText().strip().split(" ")[0]
            DATE = datetime.now() - timedelta(days=int(age))
            output = {'URL': json_data['classified']['url'],
                    'PRIX': json_data['vehicle']['price']['price'],
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
    
    
    def __init__(self, search_url):
        self.search_url = search_url
        self.page_url = []
        self.ad_url = []
        
        self.get_page_urls(search_url)
        
    
    def get_page_urls(self, url):
        """ from a given search URL, retrieve all pagination urls """
        url = self.search_url
        
        while url:
            self.page_url.append(url)
            session = GetHtmlSession(url)
            url = self.get_next_page_url(session.get_html_text())


          
    def get_ad_urls(self):
        """ return a list with urls for all ads """
        for url in self.page_url:
            
        
        
    @soup
    def get_next_page_url(self, html, **kwargs):
        """ returns url of next page """
        for e in kwargs['soup'].find_all("li", {"class": "arrow-btn"}):
            if "suivante" in e.decode_contents():
                return self.domain.format(e.find("a")['href'])
        return None





















