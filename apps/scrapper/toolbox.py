from .models import Cible
from datetime import datetime, timedelta
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import json
from django.conf import settings



# Decorator that makes soup from html
def soup(func):
    def get_soup(*args, **kwargs):
        kwargs['soup'] = BeautifulSoup(args[1], "html.parser")
        return func(*args, **kwargs)
    return get_soup


def toolbox_chooser(base_url):
    """ from a given netloc, returns the right toolbox """
    
    if base_url.netloc == "www.lacentrale.fr":
        return LacentraleToolbox(base_url)

    elif base_url.netloc == "www.leboncoin.fr":
        return LeboncoinToolbox(base_url)

    else:
        return None



class LacentraleToolbox:

    """ 
    provide set of functions to manage all scrap cycle for this source:
    -> from an index page, get all add urls
    -> from an index page, get next page url
    -> from an ad page, get data into a dict
    """
    
    def __init__(self, base_url):
        self.base_url = base_url
        self.is_async = False
    
    @soup
    def get_ad_urls(self, html, **kwargs):
        """ from a index html, returns all ad urls """

        url_list = []
        for e in kwargs['soup'].find_all("div", {"class": "adContainer"}):
            sub_soup = BeautifulSoup(e.decode_contents(), "html.parser")

            temp_ad_url = self.base_url._replace(path=sub_soup.find("a")['href'])
            url_list.append(temp_ad_url)
            
        return url_list

    
    @soup
    def get_next_page_url(self, html, **kwargs):
        """ 
        from a index html, returns next page url if exists, 
        or returns None 
        """

        try:
            return kwargs['soup'].find("a", {"title": "Page suivante"})['href']
        except:
            return None


    @soup
    def get_data_from_html(self, html, **kwargs):
        """ 
        from an ad html, retunrs a dict with data
        or None 
        """

        try:
            #  print("KWARGS :", type(kwargs['soup']))
            json_data = json.loads(kwargs['soup'].find("label", {"id": "trackingStateContainer"}).getText())
            age = kwargs['soup'].find("div", {"class": "cbm-toolboxButtons"}).span.strong.getText()
            age = age.strip().split(" ")[0]
            DATE = datetime.now() - timedelta(days=int(age))
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
            return None




class LeboncoinToolbox:

    """ 
    provide set of functions to manage all scrap cycle for this source:
    -> from an index page, get all add urls
    -> from an index page, get next page url
    -> from an ad page, get data into a dict
    """
    
    def __init__(self, base_url):
        self.base_url = base_url
        self.is_async = True 
    
    @soup
    def get_ad_urls(self, html, **kwargs):
        """ from a index html, returns all ad urls """

        url_list = []
        for e in kwargs['soup'].find_all("a", {"class": "clearfix trackable"}):
            temp_ad_url = self.base_url._replace(path=e['href'])
            url_list.append(temp_ad_url)

        return url_list
        

    @soup
    def get_next_page_url(self, html, **kwargs):
        """ 
        from a index html, returns next page url if exists, 
        or returns None 
        """

        try:
            return kwargs['soup'].find("a", {"class": "_1f-eo"})['href']
        except:
            return None


    @soup
    def get_data_from_html(self, html, **kwargs):
        """ 
        from an ad html, retunrs a dict with data
        or None 
        """

        try:
            json_data = json.loads(kwargs['soup'].find("script", {"id": "__NEXT_DATA__"}).contents[0])
            #  age = kwargs['soup'].find("div", {"class": "cbm-toolboxButtons"}).span.strong.getText()
            #  age = age.strip().split(" ")[0]
            str_date = json_data['props']['pageProps']['ad']['first_publication_date'] 
            DATE = datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S")

            attributes = {}
            attribute_list = json_data['props']['pageProps']['ad']['attributes']
            for e in attribute_list:
                attributes[e['key']] = e['value']

            ENERGIE_MAP = {'1': 'ESSENCE', 
                           '2': 'DIESEL'}

            output = {'PRIX': json_data['props']['pageProps']['ad']['price'][0],
                      'MARQUE': attributes['brand'].upper(),
                      'MODELE': attributes['model'].upper(),
                      'ENERGIE': ENERGIE_MAP[attributes['fuel']],
                      'ANNEE': attributes['regdate'],
                      'CODEPOSTAL': json_data['props']['pageProps']['ad']['location']['zipcode'],
                      'DIN': attributes['horse_power_din'],
                      'KM': attributes['mileage'],
                      'DATE': DATE}
            return output
                    
        except Exception as err:
            settings.LOGGER.error(f"leboncoin {err}")
            return None










