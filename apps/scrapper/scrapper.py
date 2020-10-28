from requests_html import AsyncHTMLSession
from datetime import datetime, timedelta
from apps.annonce.models import Annonce 
from fake_useragent import UserAgent
from .toolbox import toolbox_chooser
from urllib.parse import urlparse
from django.conf import settings
from bs4 import BeautifulSoup
from .models import Url
import itertools as it
import requests
import random
import time
import json
import os

import asyncio
import nest_asyncio


class GetHtmlSession:
    """ Build session and retrieve html source """
    
    def __init__(self, url, is_async=False, **kwargs):
        self.proxy_count = 0
        self.proxy_num = 0
        self.user_agent = UserAgent()
        self.status_code = 0
        self.err = ''
        self.url = urlparse(url)
        self.is_async = is_async
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
        
    def set_session(self, session):
        """ set proxies and headers """

        session.proxies = {"http": f"http://{self.get_proxy_http()}", 
                           "https": f"https://{self.get_proxy_https()}"}
        headers = requests.utils.default_headers()
        headers.update({'User-Agent': self.user_agent.random})
        session.headers = headers

        return session

        
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
            session = self.set_session(session)

            # Submit request
            try:
                time.sleep(random.randrange(self.min_sleep_time,self.max_sleep_time))

                if self.is_async:
                    nest_asyncio.apply()
                    loop = asyncio.get_event_loop()
                    self.response = loop.run_until_complete(self.get_async_response())
                else:    
                    self.response = session.get(self.url.geturl(), timeout=self.session_timeout)


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
                settings.LOGGER.error(f"url {self.url.geturl()}")
                break
                
            try_count += 1


    async def get_async_response(self):
        """

        """
        asession = AsyncHTMLSession()
        #  asession = self.set_session(asession)
        aresponse = asession.get(self.url.geturl())
        return await aresponse


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
            

class AnnonceListScrapper:
    """ from a annonce searche url, get all page in pagination,  """

    
    def __init__(self, index_url, **kwargs):
        self.index_url = urlparse(index_url)
        self.base_url = self.get_base_url()
        self.url_list = []
        self.kwargs = kwargs
        self.has_next = True
        self.save_count = 0
        self.toolbox = toolbox_chooser(self.base_url)
        self.is_async = self.toolbox.is_async

        self.get_urls()
        


    def get_urls(self):
        """ main function """
        
        while self.has_next:
        
            # get page html
            session = GetHtmlSession(self.index_url.geturl(), self.is_async)
            index_html = session.get_html_text()
            
            # get page urls
            url_list = self.toolbox.get_ad_urls(index_html)
            
            # record page urls
            self.record_annonce_url(url_list)
            
            # set new index url
            next_page_path = self.toolbox.get_next_page_url(index_html)
            if next_page_path:
                self.index_url = self.base_url._replace(path=next_page_path)
                print("DEBUG NEXT PAGE :", self.index_url)
                
            else:
                self.has_next = False
                

    def record_annonce_url(self, url_list):
        """ from a given url, record it in DB """
        
        # Loop over ad url list and save them
        # Not using Django's bulk_create() as the process is very slow due to scrapping bot
        for url in url_list:
            temp_url = Url(URL=url.geturl())
            print("DEBUG RECORD URL :", temp_url)
            print("DEBUG RECORD URL :", url.geturl())
            try:
                temp_url.save()
                self.save_count += 1
            except Exception as err:
                settings.LOGGER.error(f"save annonce url error {err}")
                
    
    def get_base_url(self):
        """ returns the base url of index """
        
        base_url = self.index_url._replace(path='')
        base_url = base_url._replace(query='')
        return base_url._replace(fragment='')   
    

    def success_log_record(self):
        settings.LOGGER.info(f"Annonce list scrapper: {try_count} annonces saved")
  


class AnnonceScrapper:
    """ from a given ad url, scrape data into annonce table  """
    
    def __init__(self, url):
        self.url_object = url
        self.url_parsed = urlparse(url.URL)     
        self.toolbox = toolbox_chooser(self.url_parsed)  
        self.is_async = self.toolbox.is_async

        self.get_data_from_url()
        self.save_annonce()


    def get_data_from_url(self):
        """ scrape data from url """
        
        session = GetHtmlSession(self.url_parsed.geturl(), self.is_async)
        html = session.get_html_text()
        self.data_dict = self.toolbox.get_data_from_html(html)


    def save_annonce(self):
        """ save data from dict into annonce table """
        
        try:
            annonce = Annonce(**self.data_dict)
            annonce.URL = self.url_object
            annonce.save()
            Url.objects.filter(pk=self.url_object.pk).update(STATUS = 'VALIDE')
            
        except Exception as err:
            settings.LOGGER.error(f"save annonce error : {err} for {self.url_parsed.geturl()}")
            Url.objects.filter(pk=self.url_object.pk).update(STATUS = 'ERREUR')

















