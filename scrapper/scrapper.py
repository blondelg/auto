from fake_useragent import UserAgent
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
        self.get_proxies()
        self.status_code = 0
        self.get_response()
        
        
    def get_response(self):
        """ 
        Submit request until response is 200 
        Use proxies and User agent
        """
        
        while self.status_code != 200:

            session = requests.Session()
            session.proxies = {"http": f"http://{self.get_proxy_http()}", 
                               "https": f"https://{self.get_proxy_https()}"}
            headers = requests.utils.default_headers()
            headers.update({'User-Agent': self.ua},)
            session.headers = headers
            session.timeout = 5
            
            self.response = requests.get(self.url)
            self.status_code = self.response.status_code
            time.sleep(random.randrange(1,5))



    def get_proxies(self):
        """ Get proxies list """
        
        url_http = 'https://www.proxy-list.download/api/v1/get?type=http'
        response = requests.get(url)
        proxy_list = response.text.split("\r\n")
        self.proxy_pool_http = it.cycle(proxy_list)

        url_https = 'https://www.proxy-list.download/api/v1/get?type=https'
        response = requests.get(url)
        proxy_list = response.text.split("\r\n")
        self.proxy_pool_https = it.cycle(proxy_list)
        
        self.proxy_num = len(proxy_list)
        self.proxy_count = 0

        
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
            
            
