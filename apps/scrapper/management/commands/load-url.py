from django.core.management.base import BaseCommand, CommandError
from apps.scrapper.scrapper import AnnonceListScrapper
from apps.scrapper.models import Url


class Command(BaseCommand):
    help='from a search URL, load all add urls'

    def add_arguments(self, parser):
        parser.add_argument('url', nargs='+', type=str)
        parser.add_argument(
           '--all', 
           '-a',
           action='store_true', 
           help='load all ad urls from a give search url',
        )        
        parser.add_argument(
           '--one', 
           '-o',
           action='store_true', 
           help='load one url inputed',
        )        


    def handle(self, *args, **options):
        if options['all']:
            url = Url(URL = options['url'][0])
            AnnonceListScrapper(url.URL)

        if options['one']:
            url = Url(URL = options['url'][0])
            # get target from URL
            # save url
