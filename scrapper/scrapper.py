from fake_useragent import UserAgent
from django.conf import settings
from bs4 import BeautifulSoup
import itertools as it
import requests
import random
import time
import json



class GetHtmlSession:
    """ Build session and retrieve html source """
    
    def __init__(self, url):
        self.proxy_count = 0
        self.proxy_num = 0
        self.url = url
        self.ua = UserAgent().random
        self.status_code = 0
        self.session_timeout = int(settings.CONFIG['SETTINGS']['session_timeout'])
        self.max_proxy_try = int(settings.CONFIG['SETTINGS']['max_proxy_try'])
        
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
            headers.update({'User-Agent': self.ua},)
            session.headers = headers
            
            # Submit request
            try:
                self.response = requests.get(self.url, timeout=self.session_timeout)
                self.status_code = self.response.status_code
                time.sleep(random.randrange(1,5))
                
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
    """  """
    
    def __init__(self):
        pass
        
    def scrap_lacentrale(self, html):
    
        soup = BeautifulSoup(html, "html.parser")
        try:
            json_data = json.loads(soup.find("div", {"id": "trackingStateContainer"}).getText())
            age = soup.find("div", {"class": "cbm-toolboxButtons"}).span.strong.getText().strip().split(" ")[0]
            output = {'url': json_data['classified']['url'],
                    'prix': json_data['vehicle']['price']['price'],
                    'marque': json_data['vehicle']['make'],
                    'model': json_data['vehicle']['model'],
                    'energie': json_data['vehicle']['energy'],
                    'année': json_data['vehicle']['year'],
                    'codepostal': json_data['vehicle']['zipcode'],
                    'puissance': json_data['vehicle']['powerDIN'],
                    'km': json_data['vehicle']['mileage'],
                    'age': age}
            return self.data_parser.scrap_lacentrale(self.html_full)
                    
        except Exception as err:
            settings.LOGGER.error(f"lacentrale {err}")
            return {}

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
